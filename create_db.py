#!/usr/bin/python3
import sqlite3
import os
import logging
from pathlib import Path

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


def initialize_database(filename):
    logging.info('Creating database...')
    try:
        database = sqlite3.connect(filename)
    except Exception as e:
        logging.exception(e)
    else:
        logging.info('Database created.')
        cursor = database.cursor()

        return database, cursor

if __name__ == '__main__':
    crop_dir = Path.cwd() / 'crop'    

    initial_query = '''
        CREATE table aircraft_data (
        id INTEGER PRIMARY KEY NOT NULL,
        filename CHAR(200) NOT NULL,
        class CHAR(50))
    '''

    fill_query = '''
        INSERT INTO aircraft_data 
        (filename, class)
        VALUES (?, ?)
    '''
    
    database, cursor = initialize_database('upload_data.sqlite')
    cursor.execute(initial_query)

    for item in traverse_directories(crop_dir):
        cursor.execute(fill_query, item)
        database.commit()

    cursor.close()
    