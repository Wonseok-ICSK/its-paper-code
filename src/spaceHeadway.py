# track 별 차량 / 트럭의 평균 headway를 구하는 방법 => 이거 ttc 같은 지표를 확인해볼까?
# dhw가 distance headway(m)로 앞차와의 거리를 나타내는 지표임. thw(s, 13)는 time으로 상대적인 시간을 나타냄. 
# 특정 Frame 에서 앞 차와의 거리. 앞 idx 와의 거리?
import csv
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

g_c = []
g_t = []

for track in tqdm(tracks, desc="Progress : "):
  max_vehicle = -1

  recordingMeta_csv = 'data/' + str(track) + '_recordingMeta.csv'
  tracksMeta_csv = 'data/' + str(track) + '_tracksMeta.csv' 
  tracks_csv = 'data/' + str(track) + '_tracks.csv' 

  with open(recordingMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
      max_vehicle = int(row[10])
  
  vehData = [[] for i in range(max_vehicle + 1)]
  carsId = []
  trucksId = []

  with open(tracksMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
      if row[6] == 'Car':
        carsId.append(int(row[0]))
      elif row[6] == 'Truck':
        trucksId.append(int(row[0]))


  df = pd.read_csv(tracks_csv)
  
  df.drop(['x', 'y', 'width', 'height', 'yVelocity', 'yAcceleration', 'xAcceleration', 'frontSightDistance', 'backSightDistance', 'precedingXVelocity', 'leftPrecedingId', 'followingId', 'leftAlongsideId', 'leftFollowingId', 'rightPrecedingId', 'rightAlongsideId', 'rightFollowingId', 'ttc', 'precedingId', 'laneId'], axis=1, inplace=True) # delete 

  groupById = df.groupby('id')

  car_avg_headway = []
  truck_avg_headway = []

  for id, data in groupById:
    col_headway = data['dhw']
    col_speed = data['xVelocity']

    non_zero = col_headway[col_headway != 0].tolist()
    
    vehData[id].extend(non_zero)

    if non_zero:
      avg_headway = sum(vehData[id]) / len(vehData[id])
      avg_time_headway = avg_headway / col_speed.iloc[0] if col_speed.iloc [0] != 0 else 0

      if id in carsId:
        car_avg_headway.append(avg_headway)
      elif id in trucksId:
        truck_avg_headway.append(avg_headway)

  ch = sum(car_avg_headway) / len(car_avg_headway)
  th = sum(truck_avg_headway) / len(truck_avg_headway)
  g_c.append(ch)
  g_t.append(th)

# c = sum(g_c) / len(g_c)
# t = sum(g_t) / len(g_t)
# print(f'g_c : {c:.1f}  g_t : {t:.1f}')

  plt.figure(figsize=(13, 10), dpi=150)
  
  plt.rcParams.update({'font.size' : 22})

  plt.text(x = 0.97, y = 0.85, s = f'Average car headway {ch:.2f} m\nAverage truck headway {th:.2f} m', ha='right', va='top', fontsize=12, color='black', transform=plt.gca().transAxes)

  plt.hist([car_avg_headway, truck_avg_headway], bins=25 ,label=['car', 'truck'])

  plt.title(f'Track {track} average headway')

  plt.legend()

  plt.xlabel('Average Headway(m)')

  plt.ylabel('Count(Veh)')

  plt.savefig(f'headway/b_track{track}_desc.png')#, bbox_inches='tight')

  plt.close()
