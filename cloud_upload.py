#!/usr/bin/python3
import os
import logging
from dotenv import load_dotenv
from google.cloud import storage
from pathlib import Path

# setup
load_dotenv()


# NOTE: there are 13,142 images. 
# recreating the database will add duplicate 
# filenames due to multiple objects in image

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logging.txt'
)

logging.debug('Start of upload_script.py')

def traverse_directories(dir):
    dir_list = os.listdir(dir)
    classname = None
    filename = None

    for folder in dir_list:
        classname = os.path.basename(folder)
        subdir_list = os.listdir(Path(dir) / folder)
        for file in subdir_list:
            filename = os.path.basename(file)
            yield filename, classname


def upload_to_gcs(blob_name, blob_path, bucket_name, credentials):
    logging.debug('Start of upload_to_gcs')
    # initialize Google Cloud Storage client
    gcs_client = storage.Client.from_service_account_json(credentials)

    # target bucket
    bucket = gcs_client.bucket(bucket_name)

    # upload file to bucket
    blob = bucket.blob(blob_name)

    exists_in_storage = storage.Blob(bucket=bucket, name=blob_path).exists(gcs_client)
    
    if exists_in_storage:
        logging.info('File already exists in cloud storage.')
        return (None, None)

    else:

        try:
            logging.info('Uploading file...')


            blob.upload_from_filename(blob_path)

        except Exception as e:
            status_code = e.response.status_code
            status_desc = e.response.json()['error']['message']
        else:
            status_code = 200
            status_desc = 'success'
        finally:
            return status_code, status_desc


if __name__ == '__main__':
    crop_dir = Path.cwd() / 'crop'    

    BUCKET_NAME = os.getenv('BUCKET_NAME')
    CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE')

    try:
        for filename, classname in traverse_directories(crop_dir):
            blob_path = crop_dir / classname / filename
            blob_path = blob_path.as_posix()
            upload_status = upload_to_gcs(
                blob_name=filename, blob_path=blob_path, 
                bucket_name=BUCKET_NAME, credentials=CREDENTIALS_FILE
            )
            assert upload_status == (200, 'success') or (None, None)
            logging.debug(f'{upload_status}')

    except AssertionError as a:
        logging.exception(a)

    else: 
        logging.info('File uploaded successfully or already exists.')
