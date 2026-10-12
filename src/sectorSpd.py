# Plot truck speed observations by recording and lane.
# Input/output paths and recording selections are local research settings.
import csv

import matplotlib.pyplot as plt

from tqdm import tqdm

# 차량과 트럭의 평균속도를 따로 기록할 수 있다면??

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

FRAME = 0
ID = 1
X_POS = 2
X_SPD = 4
LANE = 6

FPS = 25

LOC_DETECTOR_A = 50
LOC_DETECTOR_B = 200
LOC_DETECTOR_C = 350

for idx in tqdm(tracks, desc='Progress '):
  lane_data = [[] for _ in range(9)]

  max_idx = 0
  max_frame = 0
  max_car = 0
  max_truck = 0

  tracks_csv = 'newData/T' + str(idx) + '_tracks.csv' # 여기
  recordingMeta_csv = '../data/' + str(idx) + '_recordingMeta.csv'

  with open(recordingMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
      max_idx = int(row[10]) #num of vehicle
      max_car = int(row[11]) #num of cars
      max_truck = int(row[12]) #num of trucks
      max_frame = int(float(row[7]) * FPS) # duration

  with open(tracks_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
      lane_data[int(row[LANE])].append(row)

  for N_LANE in range(2, 9): # LANE 별 따로 보겠다.
    if N_LANE == 5: # 빈 레인임.
      continue

    plt.figure(figsize=(20, 12), dpi=200)
    plt.rcParams.update({'font.size' : 22})
    plt.title('TRACK ' + str(idx) + ' Lane' + str(N_LANE) + ' Trucks Speed') # 여기
    plt.xlabel('Seconds')
    plt.ylabel('Velocity')
    
    max_seconds = int((max_frame + 1)/ 25)
    detectors = [[] for _ in range(3)]
    
    spotted = False

    for row in lane_data[N_LANE]:
      currPos = float(row[X_POS])
      currSpd = float(row[X_SPD]) * 3.6 # m/s -> km/h
      currFrame = int(row[FRAME])
      currTime = currFrame / FPS
      direction = 0 if currSpd >= 0 else 1
      currSpd = abs(currSpd)

      if direction == 0:
        if 49 <= currPos <= 51:
          detectors[0].append((currTime, currSpd))
          plt.scatter(currTime, currSpd, c='r')
          spotted = True
        elif 199 <= currPos <= 201:
          detectors[1].append((currTime, currSpd))
          plt.scatter(currTime, currSpd, c='g')
          spotted = True
        elif 349 <= currPos <= 351:
          detectors[2].append((currTime, currSpd))
          plt.scatter(currTime, currSpd, c='b')
          spotted = True
      
      elif direction == 1:
        if 49 <= currPos <= 51:
          detectors[0].append((currTime, currSpd))
          plt.scatter(currTime, currSpd, c='b')
          spotted = True
        elif 199 <= currPos <= 201:
          detectors[1].append((currTime, currSpd))
          plt.scatter(currTime, currSpd, c='g')
          spotted = True
        elif 349 <= currPos <= 351:
          detectors[2].append((currTime, currSpd))
          plt.scatter(currTime, currSpd, c='r')
          spotted = True

    if not spotted:
      continue
    
    minSpd = detectors[0][0][1]
    maxSpd = detectors[0][0][1]

    for row in detectors:
      for _, spd in row:
        minSpd = min(spd, minSpd)
        maxSpd = max(spd, maxSpd)

    if direction == 0:
      for i, color in enumerate(['r', 'g', 'b']):
        x = [point[0] for point in detectors[i]]
        y = [point[1] for point in detectors[i]]
        if i == 0:
          desc = "50m detector"
        elif i == 1:
          desc = "200m decetor"
        elif i == 2:
          desc = "350m decetor"
        plt.plot(x, y, c=color, label=desc)

    elif direction == 1:
      for i, color in enumerate(['b', 'g', 'r']):
        x = [point[0] for point in detectors[i]]
        y = [point[1] for point in detectors[i]]
        if i == 2:
          desc = "50m detector"
        elif i == 1:
          desc = "200m decetor"
        elif i == 0:
          desc = "350m decetor"
        plt.plot(x, y, c=color, label=desc)

    plt.xlim(0, max_seconds + 10)
    plt.ylim(minSpd - 5, maxSpd + 5)
    plt.legend(loc='upper left')
    plt.savefig(f'speed/T{str(idx)}_lane{str(N_LANE)}.png') # 여기
    plt.close()

print('taskFinished')