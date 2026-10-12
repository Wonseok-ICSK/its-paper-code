# Inspect recording metadata to identify the recording/site mapping.
# Input/output paths and recording selections are local research settings.
import csv

for idx in range(10,61):
  file_name = '../data/' + str(idx) + '_recordingMeta.csv'

  with open(file_name, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
        print(str(idx), row[2])