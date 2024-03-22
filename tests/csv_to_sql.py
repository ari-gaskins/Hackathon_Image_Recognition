import csv, os, sqlite3
from pathlib import Path

# CSV header format:
#filename,width,height,class,xmin,ymin,xmax,ymax
source_path = Path.home()/'Documents'/'Hackathon_Image_Recognition'/'dataset'/'csv'
source_files = os.listdir(source_path)

print('Creating database...')
database = sqlite3.connect('dataset.sqlite')
print('Database created.')
cursor = database.cursor()

# create dataset table
print('Creating table(s)...')
cursor.execute(
    '''CREATE table aircraft_data (
        id INTEGER PRIMARY KEY NOT NULL,
        filename CHAR(200) NOT NULL,
        width INTEGER,
        height INTEGER,
        class CHAR(50),
        xmin INTEGER,
        ymin INTEGER,
        xmax INTEGER,
        ymax INTEGER
    )'''
)
print('Table(s) created.')

print('Transferring data...')
for file in source_files:
    with open(source_path/file) as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1:
                continue
            cursor.execute(
                '''INSERT INTO aircraft_data 
                (filename,width,height,class,xmin,ymin,xmax,ymax) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                tuple(row)
            )
            database.commit()

print('Data transfer completed.')

database.close()
print('Database closed.')


            
