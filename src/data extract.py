import matplotlib.pyplot as plt
import csv
from tqdm import tqdm
import json
import os

location, spdLimit, day, numVehs, numCars = "", "", "", "", ""

tracks = [11,12,13,14
,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

l1 = []
l2 = []
l3 = []
l4 = []
l5 = []
l6 = []

X_SPD = 6

g_minSpd = 100.0
g_maxSpd = 0.0

for track in tqdm(tracks, desc = 'Progress : '): # TRACK  
  c_meanSpd = 0.0
  t_meanSpd = 0.0
  
  if track < 10:
    tracks_csv = '../data/0' + str(track) + '_tracks.csv' # 
    recordingMeta_csv = '../data/0' + str(track) + '_recordingMeta.csv' # location, spdLimit, day, time, 
    tracksMeta_csv = '../data/0' + str(track) + '_tracksMeta.csv' # meanVel, 
  else:
    tracks_csv = '../data/' + str(track) + '_tracks.csv' # 
    recordingMeta_csv = '../data/' + str(track) + '_recordingMeta.csv' # location, spdLimit, day, time, 
    tracksMeta_csv = '../data/' + str(track) + '_tracksMeta.csv' # meanVel, 
  

  # print(f'Now processing track {track}')
  with open(tracks_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)
    for row in data:
      currSpd = abs(float(row[X_SPD]))

      g_maxSpd = max(g_maxSpd, currSpd)
      if g_minSpd > currSpd:
        if currSpd < 1.0:
          print(f'curr spd is {currSpd} at track {track} line{str(row[24])} at frame {row[0]} idx {row[1]}')
        g_minSpd = currSpd

#      g_minSpd = min(g_minSpd, currSpd)


print(f'maxSpd = {g_maxSpd}, minSpd = {g_minSpd}')

"""
  with open(recordingMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)
    for row in data:
      location = row[2]
      numVehs = row[10]
      numCars = row[11]
      day = row[5] + ', ' + row[4] + ' ' + row[6]
      if location == "1":
        print(track)
        if row[5] == "Mon":
          l1.append(int(numVehs))
        elif row[5] == "Wed":
          l2.append(int(numVehs))
        elif row[5] == "Thu":
          l3.append(int(numVehs))

  with open(tracksMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)
    i = 0

  #print('사례지 ' + str(track) + ', 장소 ' + location + ', 날자 ' + day + ', 총 차량 수 ' + numVehs + ', 차량 비율 ' + str(round(1 - (int(numVehs) - int(numCars))/int(numVehs), 2)) + ', 차량의 평균 통행속도 ' + str(round(c_meanSpd / int(numCars), 2)) + ', 트럭의 평균 통행 속도 ' + str(round(t_meanSpd / (int(numVehs) - int(numCars)), 2)))
  #print('')

print('avg values 1 ' + str(sum(l1) / len(l1)))
print('avg values 2 ' + str(sum(l2) / len(l2)))
print('avg values 3 ' + str(sum(l3) / len(l3)))


print('avg values 4 ' + str(sum(l4) / len(l4)))
print('avg values 5 ' + str(sum(l5) / len(l5)))
print('avg values 6 ' + str(sum(l6) / len(l6)))

      if row[6] == 'Car':
        c_meanSpd += float(row[11])
      elif row[6] == 'Truck':
        t_meanSpd += float(row[11])
  
"""