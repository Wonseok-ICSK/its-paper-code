# track 별 차량 / 트럭의 평균 headway를 구하는 방법 => 이거 ttc 같은 지표를 확인해볼까?
# dhw가 distance headway(m)로 앞차와의 거리를 나타내는 지표임. thw(s, 13)는 time으로 상대적인 시간을 나타냄. 
# 특정 Frame 에서 앞 차와의 거리. 앞 idx 와의 거리?
import csv
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

car_sum = []
truck_sum = []

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

    col_speed = col_speed[col_headway != 0]
    non_zero = col_headway[col_headway != 0]
    
    vehData[id].extend(non_zero)

    if not non_zero.empty:
      avg_speed = col_speed.abs().mean() # 이거 말고, 해당 id에 대한 음.. 아 ? 맞나? 어짜피 id 별로 들어오니까
      #맞을수도 있고, 아무튼 해당 id의 평균 ㄱㅄ으로 아 그러면 
#      avg_time_headway = avg_headway / col_speed.iloc[0] if col_speed.iloc [0] != 0 else 0 이 코드도 맞을 수 있으니까
# 이따 갔다와서 보자.
      avg_headway = non_zero.mean()

      if id in carsId:
        car_avg_headway.append(avg_headway / avg_speed)
      elif id in trucksId:
        truck_avg_headway.append(avg_headway / avg_speed)

  ch = sum(car_avg_headway) / len(car_avg_headway)
  th = sum(truck_avg_headway) / len(truck_avg_headway)

  car_sum.append(ch)
  truck_sum.append(th)

print(f'Average car headway {sum(car_sum) / len(car_sum)} sec\nAverage truck headway {sum(truck_sum) / len(truck_sum)} sec')

'''
  plt.figure(figsize=(13, 10), dpi=150)

  plt.rcParams.update({'font.size' : 22})

  plt.text(x = 0.97, y = 0.85, s = f'Average car headway {ch:.2f} sec\nAverage truck headway {th:.2f} sec', ha='right', va='top', fontsize=16, color='black', transform=plt.gca().transAxes)

  plt.hist([car_avg_headway, truck_avg_headway], bins=25 ,label=['car', 'truck'])

  plt.title(f'Track {track} average headway')

  plt.legend()

  plt.xlabel('Average Headway(sec)')

  plt.ylabel('Frequency')

  plt.savefig(f'headway/time_b_track{track}.png')# , bbox_inches='tight')

  plt.close()
'''