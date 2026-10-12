"""
row 0 : frame(time)
row 1 : 차량 id
row 2 : 차량 x 좌표

frame info 25fps

검지기 아이디어
구간 a, b, c 선정: eg. 100, 200, 300
x 좌표가 설정한 구간 좌표보다 커지는 순간, 좌표기의 X 누적
검지기 리스트에 (id, spd, etc) 추가
N-curve는 len(검지기)

생각해볼 점: 중간에 합류한 차량은 검지기에 걸리면 안되지 않나?
...
"""

import matplotlib.pyplot as plt
import csv

from tqdm import tqdm

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

FRAME = 0
ID = 1
X_POS = 2
X_SPD = 6
LANE = 24

#초당 25프레임의 비디오
FPS = 25
MAXLANE = 1

for idx in tqdm(tracks, desc='Progress '):
  max_idx = 0
  max_frame = 0

  file_name = '../data/' + str(idx) + '_tracks.csv' #
  with open(file_name, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)
    for row in data:
      if max_idx < int(row[ID]):
        max_idx = int(row[ID])
      if max_frame < int(row[FRAME]):
        max_frame = int(row[FRAME])
      if MAXLANE < int(row[LANE]):
        MAXLANE = int(row[LANE]) 

  sample = [[]for i in range(max_idx)]
  
  #print('init complete.')
  
  #print('now processing TRACK ' + str(idx) + '\tmax idx : ' + str(max_idx))

  plt.figure(figsize=(20, 12), dpi=200)
  plt.rcParams.update({'font.size' : 22})
  plt.xlabel('sec')
  plt.ylabel('vehicle')

  with open(file_name, newline='') as csvfile: # LANE
    next(csvfile)
    data = csv.reader(csvfile)
    treshold = 3

    detectorA = [0] * (max_frame + 1)# init
    detectorB = [0] * (max_frame + 1) # init
    detectorC = [0] * (max_frame + 1) # init

    checkedA = [0] * (max_idx + 1) # init
    checkedB = [0] * (max_idx + 1) # init
    checkedC = [0] * (max_idx + 1) # init

    for row in data:
      t_frame = int(row[FRAME])
      t_id = int(row[ID])
      t_x_pos = float(row[X_POS])

      if float(row[X_SPD]) >= 0: # 차량의 속도 == 방향
        if 40 - treshold < t_x_pos < 50 + treshold:
          if checkedA[t_id] == 0:
              checkedA[t_id] += 1
              detectorA[t_frame] += 1
        if 200 - treshold < t_x_pos < 200 + treshold:
          if checkedB[t_id] == 0:
            checkedB[t_id] += 1
            detectorB[t_frame] += 1
        if 350 - treshold < t_x_pos < 350 + treshold:
          if checkedC[t_id] == 0:
            checkedC[t_id] += 1
            detectorC[t_frame] += 1

  #print('data extract complete.')

  for i in range(1, len(detectorA)):
    detectorA[i] += detectorA[i - 1]
    detectorB[i] += detectorB[i - 1]
    detectorC[i] += detectorC[i - 1]




  t_length = len(detectorA)

  detectorA = detectorA[::125]
  detectorB = detectorB[::125]
  detectorC = detectorC[::125]

  y_val = []
  for i in range(0, int(t_length / 25) + 1, 5):
    y_val.append(i)

  #neg -> bgr, pos -> rgb
  plt.plot(y_val, detectorA, c = 'r', linewidth = 1)    
  plt.plot(y_val, detectorB, c = 'g', linewidth = 1)    
  plt.plot(y_val, detectorC, c = 'b', linewidth = 1)    
  
  plt.xlim(0, (max_frame + 1000) / 25)
  plt.ylim(min(min(detectorA), min(detectorB), min(detectorC)) -10 , max(max(detectorA), max(detectorB), max(detectorC)) + 10)
  plt.title('TRACK ' + str(idx) + ' (+Vel)')
  #plt.savefig('paper/N-curve/track' + str(idx) + '_downStream(posSpd)_A' + '.png')
  plt.savefig('sector/smoothingN_track' + str(idx) + '_downStream(posSpd)_S' + '.png')
  plt.close()
  #print('figure saved.')
      
      

#    print('process complete.')
    
#    plt.show()

#    print('press any key to continue')

#    dump = input()

print('task finished.')

"""
  plt.plot(detectorA, y_val, c = 'r', linewidth = 1)    
  plt.plot(detectorB, y_val, c = 'g', linewidth = 1)    
  plt.plot(detectorC, y_val, c = 'b', linewidth = 1)   

  stdA = detectorA[-1] / len(detectorA)
  stdB = detectorB[-1] / len(detectorB)
  stdC = detectorC[-1] / len(detectorC)

  for i in range(1, len(detectorA)):
    detectorA[i] -= i * stdA

  for i in range(1, len(detectorB)):
    detectorB[i] -= i * stdB

  for i in range(1, len(detectorC)):
    detectorC[i] -= i * stdC





  stdA = detectorA[-1] / len(detectorA)
  stdB = detectorB[-1] / len(detectorB)
  stdC = detectorC[-1] / len(detectorC)

  for i in range(1, len(detectorA)):
    detectorA[i] -= i * stdA

  for i in range(1, len(detectorB)):
    detectorB[i] -= i * stdB

  for i in range(1, len(detectorC)):
    detectorC[i] -= i * stdC



      for i in range(0, len(detectorA), 25): # 1초마다 데이터 기록
    plt.scatter(i, detectorA[i], c = 'r', s = 1)
    plt.scatter(i, detectorB[i], c = 'g', s = 1)
    plt.scatter(i, detectorC[i], c = 'b', s = 1)
    print(i)

    stdA = detectorA[] / len(detectorA)
    stdB = detectorB[-1] / len(detectorB)
    stdC = detectorC[-1] / len(detectorC)

    for i in range(1, len(detectorA)):
      detectorA[i] -= i * stdA
      detectorB[i] -= i * stdB
      detectorC[i] -= i * stdC



      stdA = detectorA[len(detectorA) - 1] / len(detectorA)
    stdB = detectorB[len(detectorA) - 1] / len(detectorB)
    stdC = detectorC[len(detectorA) - 1] / len(detectorC)

    for i in range(1, len(detectorA)):
      detectorA[i] -= i * stdA
      detectorB[i] -= i * stdB
      detectorC[i] -= i * stdC
"""
