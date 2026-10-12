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

    detectorA = [0] * (max_frame + 1) # init
    detectorB = [0] * (max_frame + 1) # init
    detectorC = [0] * (max_frame + 1) # init

    checkedA = [0] * (max_idx + 1) # init
    checkedB = [0] * (max_idx + 1) # init
    checkedC = [0] * (max_idx + 1) # init

    for row in data:
      t_frame = int(row[FRAME])
      t_id = int(row[ID])
      t_x_pos = float(row[X_POS])

      if float(row[X_SPD]) >= 0: # 일단 양수 LANE에 대해서만 계산할 것
        if 50 - treshold < t_x_pos < 50 + treshold:
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

##히얼

  time_ticks = [i / FPS for i in range(len(detectorA))]  # 초(second)로 X 축 눈금 설정

  plt.plot(time_ticks, detectorA, c='r', linewidth=1)
  plt.plot(time_ticks, detectorB, c='g', linewidth=1)
  plt.plot(time_ticks, detectorC, c='b', linewidth=1)

  plt.xlim(0, (max_frame + 1000)/25)
  plt.ylim(min(min(detectorA), min(detectorB), min(detectorC)) -10 , max(max(detectorA), max(detectorB), max(detectorC)) + 10)
  plt.title('TRACK ' + str(idx) + ' (+Vel)')
  plt.savefig('N-curve/original_track' + str(idx) + '_downStream(posSpd)' + '.png', bbox_inches='tight', pad_inches=0.7)
  plt.close()
  #print('figure saved.')
      

#    print('process complete.')
    
#    plt.show()

#    print('press any key to continue')

#    dump = input()

print('task finished.')

"""
  stdA = detectorA[-1] / len(detectorA)
  stdB = detectorB[-1] / len(detectorB)
  stdC = detectorC[-1] / len(detectorC)

  for i in range(1, len(detectorA)):
    detectorA[i] -= i * stdA

  for i in range(1, len(detectorB)):
    detectorB[i] -= i * stdB

  for i in range(1, len(detectorC)):
    detectorC[i] -= i * stdC

'''
  newA = []
  newB = []
  newC = []
  for i in range(0, len(detectorA), 25):
    newA.append(detectorA[i])
  for i in range(0, len(detectorB), 25):
    newB.append(detectorB[i])
  for i in range(0, len(detectorC), 25):
    newC.append(detectorC[i])
'''

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
