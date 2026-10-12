# Historical trajectory plotting variant using continuous color normalization.
# Input/output paths and recording selections are local research settings.
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors 
import csv
import json
import os

tracks = [11,12,13,14
,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

FRAME = 0
ID = 1
X_POS = 2
X_SPD = 6
LANE = 24

FPS = 25

max_idx = 0
max_frame = 0

for idx in tracks:
  file_name = '../data/' + str(idx) + '_tracks.csv' #
  with open(file_name, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)
    for row in data:
      if max_idx < int(row[ID]):
        max_idx = int(row[ID])
      if max_frame < int(row[FRAME]):
        max_frame = int(row[FRAME])

  sample = [[]for i in range(max_idx)]
  detectorA = [0] * max_frame
  detectorB = [0] * max_frame
  detectorC = [0] * max_frame
  
  CdetectorA = [0] * max_frame
  CdetectorB = [0] * max_frame
  CdetectorC = [0] * max_frame
  
  norm = plt.Normalize(0, 100)
  
  print('init complete.')
  
  for N_LANE in range(1, 8): # LANE
    print('now processing TRACK ' + str(idx) + '  LANE ', str(N_LANE))

    plt.figure(figsize=(55, 14), dpi=250)
    plt.xlabel('second')
    plt.ylabel('distance x')

    with open(file_name, newline='') as csvfile:
      next(csvfile)
      data = csv.reader(csvfile)
      for row in data:
        if int(row[LANE]) == N_LANE: #해당 차선에 대하여
          sample[int(row[ID]) - 1].append((row[FRAME], row[X_POS], abs(float(row[X_SPD]))))

    print('data extract complete.')

    for i in range(max_idx): 
      if not sample[i]: # 해당 id가 없으면 생략
        continue

      x_values = [int(item[0]) / FPS for item in sample[i]] # frame
      y_values = [float(item[1]) for item in sample[i]] # x_pos
      z_values = [item[2] for item in sample[i]] # x_spd

      plt.scatter(x_values, y_values, c=z_values, s=1)

      print(i)

    plt.xlim(0, max_frame/25)
    plt.ylim(-50 , 450)

    print('process complete.')
    plt.gray()
    plt.colorbar()
    plt.savefig('newSTD/T/Track' + str(idx) + '_lane'+ str(N_LANE) +'_StratToEnd.png')
    plt.close()
    print('figure saved.')

print('task finished.')