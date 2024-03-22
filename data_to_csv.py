#!/usr/bin/python3
import json
import csv
import os
import sqlite3
import logging
from dotenv import load_dotenv

# setup
load_dotenv()

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='json_logging.txt'
)

logging.debug('Start of data_jsonl.py')


def initialize_database(filename):
    logging.info('Connecting to database...')
    try:
        database = sqlite3.connect(filename) 
    except Exception as e:
        logging.exception(e)
    else:
        logging.info('Database created.')
        cursor = database.cursor()

        return cursor
    
# def data_to_dict(uri, filename, classname):
#     data = {
#         "imageGcsUri": f'{uri}/{filename}',
#         "classificationAnnotation": 
#             {"displayName": classname},
#             "annotationResourceLabels": {
#                 "aiplatform.googleapis.com/annotation_set_name": classname
#             }
#     }

#     return data



if __name__ == '__main__':
    # get database cursor
    database_file = 'upload_data.sqlite'
    cursor = initialize_database(database_file)

    query = '''
        SELECT filename, class
        FROM aircraft_data
    '''
    
    BUCKET_URI = os.getenv('BUCKET_URI')

    cursor.execute(query)
    rows = cursor.fetchall()

    with open('dataset.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)

        for filename, classname in rows:
            filename = f'{BUCKET_URI}/{filename}' 
            writer.writerow([filename, classname])

        csv_file.close()

    # with open('dataset.jsonl', 'w') as jsonl_file:
    #     for filename, classname in rows:
    #         dict_data = data_to_dict(BUCKET_URI, filename, classname)
    #         json.dump(dict_data, jsonl_file)
    #         jsonl_file.write('\n')