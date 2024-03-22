import os, shutil
from pathlib import Path

#source_path = Path.cwd()/'dataset'
# change to 'csv' for csv folder, 'images' for images folder
#destination_path = source_path/'csv'
#source_files = os.listdir(source_path)


#print('Moving files...')


#for file in source_files:
    #if file.endswith('.csv'):
    #    shutil.move(source_path/file, destination_path/file)
    #if file.endswith('.jpg'):
    #    shutil.move(source_path/file, destination_path/file)


training_path = Path.cwd()/'crop'
training_classes = os.listdir(training_path)

#class_count = 0
file_count = 0

print('Counting files...')

#for dir in training_classes:
#    for file in dir:
#        file_count += 1
#    class_count += 1 

for dir in training_classes:
    for file in dir:
        file_count += 1
    print(f'Number of files in {dir}: {file_count}')
    file_count = 0
    
print('Completed.')

#print(f'Number of classes: {class_count}')
#print(f'Number of files: {file_count}')


