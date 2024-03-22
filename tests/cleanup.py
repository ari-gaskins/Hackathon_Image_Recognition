import sqlite3


database = sqlite3.connect('dataset.sqlite')
cursor = database.cursor()

#delete_query = 'DELETE FROM aircraft_data WHERE id IN (SELECT id FROM aircraft_data ORDER BY id LIMIT 211)'

#cursor.execute(delete_query)

cleanup_query = '''
    DELETE FROM aircraft_data WHERE ROWID NOT IN
    (SELECT MIN(ROWID) FROM aircraft_data GROUP BY (filename))
'''

cursor.execute(cleanup_query)
database.commit()