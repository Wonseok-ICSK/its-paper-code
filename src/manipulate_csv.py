import pandas as pd
import csv

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

for track in tracks:
  carId = []
  tracksMeta_csv = 'data/' + str(track) + '_tracksMeta.csv' # meanVel, 

  with open(tracksMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
      if row[6] == 'Truck':
        carId.append(int(row[0]))

  filename = 'newData/M' + str(track) + '_tracks.csv'

  df = pd.read_csv(filename)

  df = df[df['id'].isin(carId)]

  savePath = 'newData/T' + str(track) + '_tracks.csv'
  df.to_csv(savePath, index=False)