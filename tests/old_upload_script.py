#!/usr/bin/python3
import sqlite3
import os
import time
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

logging.debug('Start of program')

def initialize_database(filename):
    logging.info('Creating database...')
    try:
        database = sqlite3.connect(filename)
    except Exception as e:
        logging.exception(e)
    else:
        logging.info('Database created.')
        cursor = database.cursor()

        return cursor


def yield_images(cursor, table_name):
    query = f'''
        SELECT (filename) FROM {table_name}
    '''
    try:
        cursor.execute(query)

        rows = cursor.fetchall()
        for row in rows:
            filename = row[0] + '.jpg'
            yield(filename)
            time.sleep(1)
    except Exception as e:
        logging.exception(e)


def upload_to_gcs(blob_name, bucket_name, credentials):
    logging.debug('Start of upload_to_gcs(%s%%, %s%%, %s%%)' % (blob_name, bucket_name, credentials))
    # initialize Google Cloud Storage client
    gcs_client = storage.Client.from_service_account_json(credentials)

    # target bucket
    bucket = gcs_client.bucket(bucket_name)

    # upload file to bucket
    blob = bucket.blob(blob_name)
    blob_path = Path.cwd() / 'dataset' / 'images' / f'{blob_name}'
    blob_path = blob_path.as_posix()

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


if __name__ == "__main__": 
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")

    cursor = initialize_database('dataset.sqlite')
    table_name = 'aircraft_data'

    try:
        for filename in yield_images(cursor, table_name):
            upload_status = upload_to_gcs(filename, BUCKET_NAME, CREDENTIALS_FILE)
            assert upload_status == (200, 'success') or (None, None)
            time.sleep(1)
    except AssertionError as a:
        logging.exception(a)
    else:
        logging.info('File uploaded successfully or already exists.')