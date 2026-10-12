# Generate space-time trajectory diagrams for selected recordings and lanes.
# Input/output paths and recording selections are local research settings.
"""
row 0 : frame(time)
row 1 : 차량 id
row 2 : 차량 x 좌표

frame info 25fps

location ID
track01_ 2
track02_ 2
  track03_ 2
track04_ 3
  track05_ 3
track06_ 3
track07_ 4
track08_ 4
  track09_ 4
track10_ 4
track11_ 1
track12_ 1
  track13_ 1
track14_ 1
track15_ 5
track16_ 5
track17_ 5
track18_ 5
track19_ 5
track20_ 5
  track21_ 5
track22_ 5
track23_ 5
track24_ 5
track25_ 1
track26_ 1
track27_ 1
track28_ 1
track29_ 1
track30_ 1
track31_ 1
track32_ 1
track33_ 1
track34_ 1
"""


"""
검지기 아이디어
구간 a, b, c 선정: eg. 100, 200, 300
x 좌표가 설정한 구간 좌표보다 커지는 순간, 좌표기의 X 누적
검지기 리스트에 (id, spd, etc) 추가
N-curve는 len(검지기)

생각해볼 점: 중간에 합류한 차량은 검지기에 걸리면 안되지 않나?
...
"""




import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import csv
import json
import os

colour5 = ['darkred', 'red', 'orange', 'yellow', 'lime', 'aqua', 'dodgerblue', 'blue', 'midnightblue', 'k', 'k', 'k']
            # 0-8    9-17     18-26     27-35    36-44    45-53   54-62         63-71   72-80           80+
            # 0      1        2         3        4        5       6             7       8               9

tracks = ['03'] # TRACKS, '05', '09', 13, 21, 59

FRAME = 0
ID = 1
X_POS = 2
X_SPD = 6
LANE = 24

#초당 25프레임의 비디오
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
          sample[int(row[ID]) - 1].append((row[FRAME], row[X_POS], int(abs(float(row[X_SPD])) / 9)))

    print('data extract complete.')

    for i in range(max_idx): 
      if not sample[i]: # 해당 id가 없으면 생략
        continue

      x_values = [int(item[0]) / FPS for item in sample[i]] # frame
      y_values = [float(item[1]) for item in sample[i]] # x_pos
      z_values = [item[2] for item in sample[i]] # x_spd

      for i in range(0, len(x_values), 5):
        plt.scatter(x_values[i], y_values[i], s=2, color = colour5[z_values[i]])
      print(i)

    plt.xlim(0, max_frame/25)
    plt.ylim(-50 , 450)
    #plt.show()

    print('process complete.')
    plt.savefig('newSTD/T/' + str(idx) + '_lane'+ str(N_LANE) +'_StratToEnd.png')
    plt.close()
    print('figure saved.')

print('task finished.')