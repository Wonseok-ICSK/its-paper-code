import csv
import pandas as pd
from tqdm import tqdm

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

with open(f'ToS_SoT.csv', 'w', newline='') as csvfile: # csv 파일로 저장을 위한 내용
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(['Track', '# of Truck', '# of common', '# of slow veh', 'Truck 중 저속 차량의 비율', '저속 차량 중 트럭의 비율'])

  for track in tracks: # 처음에 트럭에 해당하는 id를 받아서 넣기
    tracks_csv = 'data/' + str(track) + '_tracks.csv' 
    tracksMeta_csv = f'data/{track}_tracksMeta.csv'
    
    truck_ids = []
    slow_ids = []

    with open(tracksMeta_csv, newline='') as csvfile:
      next(csvfile)
      data = csv.reader(csvfile)

      for row in data:
        if row[6] == 'Truck':
          truck_ids.append(int(row[0])) # id 삽입

    df = pd.read_csv(tracks_csv)

    groupByLane = df.groupby('laneId')

    for lane, data in tqdm(groupByLane, desc=f'Track {track} of track {tracks[-1]} | Progress '):
      col_id = data['id'].tolist() # 하나의 lane에 있는 모든 데이터

      max_idx = data['id'].nunique()

      prec_id = data['precedingId'].tolist()

      col_speed = data['xVelocity'].tolist()
      col_speed = [abs(x * 3.6) for x in col_speed] # m/s -> km/h

      col_frame = data['frame'].tolist()

      idx_dict = {}
      c_veh_spd = [[] for _ in range(max_idx)]
      p_veh_spd = [[] for _ in range(max_idx)]
      p_veh_idx = []

      for frame, id, p_id, spd in zip(col_frame, col_id, prec_id, col_speed):
        if id not in idx_dict:
          idx_dict[id] = len(idx_dict)
        
        idx = idx_dict[id]

        if p_id != 0: # 선행 차량이 있음. 해당 id 의 frame을 찾아서, 선행 차량의 frame 에서의 현재 속도를 구하는 방법을 강구.
          prec_data = data[data['id'] == p_id]
          prec_frame_data = prec_data[prec_data['frame'] == frame]

          if not prec_frame_data.empty:
            prec_spd = prec_frame_data['xVelocity'].iloc[0]
            prec_spd = abs(prec_spd * 3.6)
            c_veh_spd[idx].append(spd)
            p_veh_spd[idx].append(prec_spd)
      
      h_idx = []
      # 한 lane의 처리가 다 끝났을 경우.
      # 현재 p_id가 똑바로 출력되지 않는 문제가 있음
      for id, idx in idx_dict.items():
        if len(c_veh_spd[idx]) != 0 and len(p_veh_spd) != 0:
          mean_c_vel = sum(c_veh_spd[idx]) / len(c_veh_spd[idx])
          mean_p_vel = sum(p_veh_spd[idx]) / len(p_veh_spd[idx])
          ratio = mean_c_vel / mean_p_vel * 100

          if ratio < 90.0: # 선행 차량 대비 평균 속도가 90% 이하
            h_idx.append(id)
            slow_ids.append(id)
      
      common_ids = set(truck_ids) & set(slow_ids)
      ToS = len(common_ids) / len(truck_ids)
      SoT = len(common_ids) / len(slow_ids)

      csvwriter.writerow([track, len(truck_ids), len(common_ids), len(slow_ids), "{:.2f}".format(ToS), "{:.2f}".format(SoT)])
  
print('Task finished ^___^)')