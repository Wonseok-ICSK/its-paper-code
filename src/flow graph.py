# Estimate and plot vehicle flow past the configured observation position.
# Input/output paths and recording selections are local research settings.
# flow graph 그리기

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

def flow(tracks, targetDist, max_idx, max_frame):
  # 그림판 생성
  plt.figure(figsize=(20, 12), dpi=200)
  plt.rcParams.update({'font.size' : 22})
  plt.xlabel('frame')
  plt.ylabel('flow')
  
  file_name = 'data/' + str(tracks) + '_tracks.csv' #
  # 데이터 읽어오기
  with open(file_name, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    header = next(csv_reader)  # 헤더를 읽어옴
    data = list(csv_reader)  # 나머지 데이터를 리스트로 저장

  sorted_data = sorted(data, key=lambda x: int(x[FRAME]))
  
 # with open(file_name, newline='') as csvfile: # LANE
 #   next(csvfile)
 #   data = csv.reader(csvfile)
  treshold = 3 # 단위(m)

  flow = [None] * (max_frame + 1)
  
  checked = [0] * (max_idx) 

  previous_frame = -1 

  for row in sorted_data:
    t_frame = int(row[FRAME]) # Time stamp.
    t_id = int(row[ID]) - 1 # id가 1번부터 생성되어서 하나 씩 당겨서 사용.
    t_x_pos = float(row[X_POS])
    t_lane = int(row[LANE])

    #if t_lane == 2:
    if float(row[X_SPD]) >= 0: # 차량의 속도 == 방향
      if targetDist - treshold < t_x_pos < targetDist + treshold: # 차량이 해당 검지기를 밟음.
        if checked[t_id] == 0: # 해당 차량이 이전에 밟은 적이 없으면
          checked[t_id] += 1 # 밟았음을 표시.
          
          if previous_frame == -1: # 야 나 처음 밟는거다?
            previous_frame = t_frame # update
          else: # 뭔가 정보가 있어
            if t_frame != previous_frame:
              flow[t_frame] = (1 / (t_frame - previous_frame)) * 100 # 앞 놈이 밟은거 - 뒷 놈이 밟은거 (이 값을 25로 나누면 second가 됨. 값이 너무 크다면 해봄직 함.)
            #print(f'id {str(t_id)} p {str(previous_frame)} t {str(t_frame)}')
            previous_frame = t_frame # update

  plt.scatter(range(len(flow)), flow, c='r', s=5)  # s parameter controls the size of the markers 
  plt.plot(flow, c = 'b', linewidth = 1)      
  
  min_flow = float('inf')
  max_flow = float('-inf')
  for i in flow:
    if i != None:
      min_flow = min(min_flow, i)
      max_flow = max(max_flow, i)

  plt.xlim(0, max_frame + 500)
  plt.ylim(min_flow -5 , max_flow + 5)
  plt.title(f'TRACK {str(tracks)} LANE {str(t_lane)} at dist {targetDist}(m) (+Vel)')
  plt.savefig(f'flow/track{str(tracks)}_downStream(posSpd)_dist {targetDist}.png')
  plt.close()

# 시작 부분
#for idx in tqdm(tracks, desc='Progress '):
for idx in tracks:
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

  for i in [50, 200, 350]:
    flow(idx, i, max_idx, max_frame)

print('task finished.')