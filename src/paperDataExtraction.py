# Prepare direction-specific trajectory data and apply the shared analysis helpers.
# Input/output paths and recording selections are local research settings.
"""
일단 해당 코드에서 해야할 일!
1. csv 파일을 읽어 적절한 Data Frame으로 변환하여 사용하여야 함
    --> 이 적절한 Data Frame의 기준은 우선 도로의 방향별로 
    upStream/downStream을 나누고 처리해야함

이 코드에서 하고 싶은건 결국 그놈의 표를 만드는 것.

일반적인 상황을 가정하고 그냥 표를 뽑는다.
각각 innerLane / middleLane / outerLane으로 나누고
다시 이걸 x1(50m) x2(200m) x3(350m) 구간으로 나눈다.

어떻게 구간으로 나누지?
아마 구간을 지나는 id를 써..?

그러면 우선 표는 나중일로 하고.
leader vehicle을 detect하는 방법
예 그걸 바탕으로 뭘 하는 법.. 에 대해 배울 겁니다.
"""

import cv
from tqdm import tqdm
import pandas as pd
import random

upstream = [2, 3, 4]
downstream = [6, 7, 8]

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS
mini_tracks = [12, 25, 26]

for track in tqdm(tracks, desc='Progress '):
  data = pd.read_csv('data/' + str(track) + '_tracks.csv')
  
  # 임시!!!!
  data = data[data['laneId'] > 5]
  
  # slowVehicle = cv.getTruckIds(track)

  # slowVehicle = cv.detectSlowVehs(data) # list
  #print('1')
  slowVehicle = cv.detectSlowVehPandas(data) # list
  '''
  print('2')

  a = set(slowVehicleo)  
  b = set(slowVehicle)
  c = a - b
  d = b - a

  print('\n\n')
  print(f'a : {a}\nb : {b}')
  print('\n\n')
  print(f'a - b : {c}\nb - a : {d}')
  print(len(c))
  print(len(d))
  print('\n\n')
  '''
  # select leader vehicle that has normal speed.
  # based on random numbergeneration.
  used = []
  temp = data['frame'].copy()
  max_frame = temp.max()
  temp = data[data['frame'] <= max_frame - 375]
  total_vehicle = temp['id'].nunique()

  for _ in range(5):
    randomLeader = random.randint(0, total_vehicle-1)

    while randomLeader not in slowVehicle and randomLeader not in used:
      randomLeader = random.randint(0, total_vehicle-1)
    used.append(randomLeader)

    # randomLeader보다 낮은 idx를 가진 데이터 제거
    selected_data = data[data['id'] >= randomLeader]

    #Leader의 Lane만 남김
    lane = selected_data['laneId'].iloc[0]
    selected_data = selected_data[selected_data['laneId'] == lane]

    #print(randomLeader)
    #print(selected_data)
    
    startFrame = selected_data['frame'].iloc[0]
    cv.toCsv(selected_data, False, randomLeader, track, startFrame)

  for _ in range(5):
    randomLeader = random.randint(0, total_vehicle-1)

    while randomLeader not in slowVehicle and randomLeader not in used:
      randomLeader = random.randint(0, total_vehicle-1)
    used.append(randomLeader)
    # randomLeader보다 낮은 idx를 가진 데이터 제거
    selected_data = data[data['id'] >= randomLeader]
    
    #Leader의 Lane만 남김
    lane = selected_data['laneId'].iloc[0]
    selected_data = selected_data[selected_data['laneId'] == lane]

    startFrame = selected_data['frame'].iloc[0]
    cv.toCsv(selected_data, True, randomLeader, track, startFrame)

"""

# randomLeader와 다른 방향의 데이터 제거
direction = selected_data['laneId'].iloc[0]
if direction in upstream:
  selected_data = selected_data[selected_data['laneId'].isin(upstream)]
else:
  selected_data = selected_data[selected_data['laneId'].isin(downstream)]

#selected_data = selected_data[selected_data['laneId'] == selected_data['laneId'].iloc[0]]

    laneId = data[(data['id'] == randomLeader)]['laneId'].iloc[0]
    selected_data = data[(data['laneId'] == laneId)]
"""