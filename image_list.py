import sqlite3
import os
from pathlib import Path

# get filename and class, format as class/filename for labeling

cwd = Path.cwd()
image_list_path = cwd / 'hello-custom-sample' / 'webapp' / 'image-list.txt'


database = sqlite3.connect('dataset.sqlite')
cursor = database.cursor()
query = '''
    SELECT DISTINCT filename, class 
    FROM aircraft_data ORDER BY id
'''

with open(image_list_path, 'wt') as image_list:
    cursor.execute(query)
    rows = cursor.fetchmany(500)
    for filename, classname in rows:
        key_val = classname + '/' + filename + '.jpg'
        image_list.write(key_val + '\n')

