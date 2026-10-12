# Integrate differences between cumulative detector counts for selected recordings.
# Input/output paths and recording selections are local research settings.
# 사실 속도가 아니고, Lane 별로 구분해도 되지 않나 싶기는 함. 
# 뭐 여기까지 왔는걸 어째

import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
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
#for idx in tracks:
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

      if float(row[X_SPD]) < 0: # 차량의 속도 == 방향  <><><>
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

  diffBtAandC = [a - c for a, c in zip(detectorC, detectorA)]

  diffBtAandC0 = [max(0, x) for x in diffBtAandC]

  diffBtAandC0 = np.cumsum(diffBtAandC0)

  result = integrate.trapezoid(diffBtAandC0)

  plt.figure(figsize=(20, 12), dpi=200)

  plt.rcParams.update({'font.size' : 22})

  plt.title(f'Track {idx} negSpd Total delay') # <><><>

  plt.xlabel('second')
  
  plt.ylabel('delay')

  plt.plot(y_val, diffBtAandC0, c='red', linewidth=2, alpha=1)
  
  plt.text(x = 0.97, y = 0.97, s = f'accumulative delay : {result:.2f} (veh*sec)', ha='right', va='top', fontsize=16, color='black', transform=plt.gca().transAxes)

  plt.savefig(f'integral/accum_Track {idx} negSpd.png', bbox_inches='tight') # <><><>

  plt.close()

print('task finished.')