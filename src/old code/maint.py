"""
row 0 : frame(time)
row 1 : 차량 id
row 2 : 차량 x 좌표

frame info 25fps

track01_ 1048
track02_ 1113
track03_ 914
track0
track0
track0
track0
track0
track0
"""

import matplotlib.pyplot as plt
import csv

color = ['black', 'gray', 'lightcoral', 'red', 'brown', 'peru', 'darkorange', 'tan', 'gold', 'olive', 'yellow', 'lawngreen', 'honeydew', 'forestgreen', 'aquamarine', 'azure', 'teal', 'deepskyblue', 'dodgerblue', 'navy', 'slateblue', 'plum', 'violet', 'purple', 'pink']
colour = ['red', 'orangered', 'darkorange', 'orange', 'gold', 'limegreen', 'lime', 'dodgerblue', 'blue', 'navy', 'midnightblue']
colour5 = ['red', 'orange', 'yellow', 'navy', 'lime', 'lime'] # black is for outlier
colours = ['red', 'orange', 'yellow', 'navy', 'lime'] 
# 각자 저장된 col 넘버
FRAME = 0
ID = 1
X_POS = 2
X_SPD = 6
LANE = 24

#초당 25프레임의 비디오
FPS = 25

N_LANE = 6

max_idx = 0

for idx in range(1, 10):
  plt.figure(figsize=(26.7, 14), dpi=150)

  file_name = '../data/0' + str(idx) + '_tracks.csv'
  with open(file_name, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)
    for row in data:
      if max_idx < int(row[ID]):
        max_idx = int(row[ID])

  print('max_idx calc complete')

  sample = [[]for i in range(max_idx)]

  min_spd = float(200)
  max_spd = float(0)

  with open(file_name, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)
    for row in data:
      if int(row[LANE]) == N_LANE: # lane 5
        if int(row[FRAME]) >= 10000: ### A
        #if int(row[FRAME]) < 10000: ### B
          continue
        cur_spd =  float(row[X_SPD])
        if cur_spd > max_spd:
          max_spd = cur_spd
        if cur_spd < min_spd:
          min_spd = cur_spd
        sample[int(row[ID]) - 1].append((row[FRAME], row[X_POS], cur_spd))

  print('data extract complete.')

  divider = float(max_spd - min_spd)

  print('divider is', str(divider))

  #for i in range(1048):
  for i in range(max_idx): 
    if not sample[i]: # 해당 id가 없으면 생략
      continue

    x_values = [int(item[0]) / FPS for item in sample[i]] # frame
    y_values = [float(item[1]) for item in sample[i]] # x_pos
    z_values = [int(((item[2]) - min_spd) * 5 / divider) for item in sample[i]] # x_spd

    print(i)
    for i in range(len(x_values)):
      plt.scatter(x_values[i], y_values[i], s=1, color = colour5[z_values[i]])

  plt.xlabel('second')
  plt.ylabel('distance x')

  #plt.show()

  plt.savefig('N-Figure_track' + str(idx) + '_lane'+ str(N_LANE) +'_10000toEnd.png')

  print('figure saved')