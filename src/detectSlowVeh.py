# Identify candidate slow vehicles and visualize their trajectories by lane.
# Input/output paths and recording selections are local research settings.
# idea : 해당 Lane 별 기대속도를 구하고, 기대속도 대비 10% 이상 낮은 차량 중, 선두에 있는 차량을 저속차량으로 분류
# 그러니까, 예를 들어 두 대가 연속으로 서행중이라면, 선두 차량만 저속차량으로 구분하고, 뒤 따르는 차량은 후속차량으로 분류
# 대신 뒤의 차는 ?
# 아이고 세상에 머가리가..
# 

import csv
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from cv import countVeh

mini_tracks = [30,31,32,33,34,35] # TRACKS
tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

def drawTrajectory(track, h_list, max_frame, spd_range, data_list: pd.DataFrame): # 해당 코드를 lane 별로 구분해서 그릴 필요가 있음.
  lane_seperate = data_list.groupby('laneId') # lane 별로 묶음.

  for lane, data in lane_seperate:
    # 그림판 설정
    plt.figure(figsize=(55, 14), dpi=250)
    plt.rcParams.update({'font.size' : 22})
    plt.xlabel('second')
    plt.ylabel('distance x')

    spd_range = [min(140.0, speed) for speed in spd_range] # 속도의 최대값 suppress.  
    norm = plt.Normalize(min(spd_range), max(spd_range))
    plt.set_cmap('gist_rainbow')

    # data를 끄집어 내는 과정.
    groupbyId = data.groupby('id')
    for id, data in groupbyId: # id 마다 반복함.
      frame_list = data['frame'].tolist() # 그러니까 이건 id에 해당하는 모든 정보를 한 번에 취합하는 거라는 이야기지.
      frame_list = [frame / 25 for frame in frame_list]
      x_pos_list = data['x'].tolist()
      speed_list = data['xVelocity'].tolist()
      speed_list = [min(140.0, abs(x * 3.6)) for x in speed_list] # m/s -> km/h + 속도의 최대값 suppress.

      # 정보를 바탕으로 그림을 그림
      if id in h_list: # 이게 맞다면, id 별로 한 줄 씩 그려나가는 프로그램이 되겠군!
        plt.scatter(frame_list, x_pos_list, c='black', s=1)
      else:
        plt.scatter(frame_list, x_pos_list, c=speed_list, s=1, vmin=0.0, vmax=140.0)
    
    # 저장 옵션 설정 및 그림판 메모리 해제
    plt.xlim(0, max_frame/25)
    plt.ylim(-50 , 450)

    plt.title(f'TRACK {str(track)} lane {lane}')
    plt.colorbar(aspect=70).set_label('Vehicle Speed(km/h)')
    plt.savefig(f'slowveh/Track{track}_lane{lane}.png', bbox_inches='tight', pad_inches=0.7)
    plt.close()

with open(f'slowveh/side_output.csv', 'w', newline='') as csvfile: # csv 파일로 저장을 위한 내용
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(['Track', 'id', 'meanVel', 'p_id', 'p_meanVel', 'mean difference', 'mean side difference', 'ratio', 'front ratio', 'side ratio', 'b_old', 'b_new', 'b_side'])

  for track in tqdm(tracks, desc='Now loading...'):
    csvwriter.writerow(['', '', '>>>>>', 'Track', f'{track}', '<<<<<', '', '', '', '', '', '', '', ''])

    tracks_csv = 'data/' + str(track) + '_tracks.csv' 

    data = pd.read_csv(tracks_csv)

    col_id = data['id'].tolist() # 하나의 lane에 있는 모든 데이터

    max_idx = data['id'].nunique() # 중복되지 않는 엘리맨트의 수

    prec_id = data['precedingId'].tolist()
    
    r_prec_id = data['rightPrecedingId'].tolist()
    l_prec_id = data['leftPrecedingId'].tolist()

    col_speed = data['xVelocity'].tolist()
    col_speed = [abs(x * 3.6) for x in col_speed] # m/s -> km/h

    col_frame = data['frame'].tolist()
    
    #col_xpos = data['x'].tolist()

    idx_dict = {}
    c_veh_spd = [[] for _ in range(max_idx)]
    p_veh_spd = [[] for _ in range(max_idx)]
    veh_spd_diff = [[] for _ in range(max_idx)]
    side_veh_spd_diff = [[] for _ in range(max_idx)]
    p_veh_idx = []

    for frame, id, p_id, spd, l_id, r_id in zip(col_frame, col_id, prec_id, col_speed, l_prec_id, r_prec_id):
      if id not in idx_dict:
        idx_dict[id] = len(idx_dict)
      
      idx = idx_dict[id]

      if p_id != 0: # 선행 차량이 있음. 해당 id 의 frame을 찾아서, 선행 차량의 frame 에서의 현재 속도를 구하는 방법을 강구.
        prec_data = data[data['id'] == p_id] # 선행 차량의 데이터를 prec_data로 가지고 옴
        prec_frame_data = prec_data[prec_data['frame'] == frame] # 이전 차량의 데이터 중 해당 프레임의 데이터만 받아옴
        if not prec_frame_data.empty: # 선행 차량의 frame 정보를 받아오는걸 성공한 경우  
          prec_spd = prec_frame_data['xVelocity'].iloc[0] # 선행 차량의 속도는 크게 변하지 않는다고 가정.. 따라서 첫 포착된 속도를 사용, 변경 가능성 있음            
          prec_spd = abs(prec_spd * 3.6)
          c_veh_spd[idx].append(spd)
          p_veh_spd[idx].append(prec_spd)
          veh_spd_diff[idx].append(prec_spd - spd)
          # p_veh_idx.append(p_id)
          # print(f'현재 차량 {id}에 대해 선행차량 {p_id}의 속도 : {prec_spd}')
        
        l_prec_data = data[data['id'] == l_id]
        l_data_at_frame = l_prec_data[l_prec_data['frame'] == frame]
        if not l_data_at_frame.empty:
          l_spd = abs(l_data_at_frame['xVelocity'].iloc[0] * 3.6)
          side_veh_spd_diff[idx].append(l_spd - spd)
          
        r_prec_data = data[data['id'] == r_id]
        r_data_at_frame = r_prec_data[r_prec_data['frame'] == frame]
        if not r_data_at_frame.empty:
          r_spd = abs(r_data_at_frame['xVelocity'].iloc[0] * 3.6)
          side_veh_spd_diff[idx].append(r_spd - spd)

    h_idx = []
    # 한 lane의 처리가 다 끝났을 경우.
    # 현재 p_id가 똑바로 출력되지 않는 문제가 있음
    for id, idx in idx_dict.items():
      # p_id = p_veh_idx[idx]

      if len(c_veh_spd[idx]) != 0 and len(p_veh_spd) != 0:
        mean_diff = sum(veh_spd_diff[idx]) / len(veh_spd_diff[idx])
        if len(side_veh_spd_diff[idx]) != 0:
          mean_s_diff = sum(side_veh_spd_diff[idx]) / len(side_veh_spd_diff[idx])
        else:
          mean_s_diff = -1
        mean_c_vel = sum(c_veh_spd[idx]) / len(c_veh_spd[idx])
        mean_p_vel = sum(p_veh_spd[idx]) / len(p_veh_spd[idx])
        ratio = mean_c_vel / mean_p_vel * 100
        
        prec_spd_ratio = mean_diff / mean_p_vel

        if not mean_s_diff == -1: 
          side_spd_ratio = mean_s_diff / mean_p_vel # 이게 p_vel인지 c_vel인지 다시 생각해볼것
        else:
          side_spd_ratio = -1        

        b_old = True if ratio < 90.0 else False
        b_new = True if prec_spd_ratio > 0.1 else False
        b_side = True if mean_s_diff != -1 and mean_s_diff / mean_p_vel > 0.05  else False
        
        # to csv
        csvwriter.writerow([track, id, mean_c_vel, p_id, mean_p_vel, mean_diff, mean_s_diff, ratio, prec_spd_ratio, side_spd_ratio, b_old, b_new, b_side])
            
        if mean_s_diff != -1: # 만약에 옆 차의 정보가 하나라도 있다면
          if prec_spd_ratio > 0.1 and side_spd_ratio > 0.05: # 좌 우 차량의 속도 편차까지 고려
            h_idx.append(id)
        else: # 그렇지 않다면
          if prec_spd_ratio > 0.1: # 기존 처럼 선행 차량의 속도만 고려
            h_idx.append(id)
        #print(f'Track {track} Lane {lane} | 내 차량{id}의 평균 속도 {mean_c_vel}, 선행 차량{p_id}의 평균 속도 {mean_p_vel}, 선행차량 대비 내 차량 속도 {ratio:.2f}')
    
    max_frame = max(col_frame)
    drawTrajectory(track, h_idx, max_frame, col_speed, data)
    countVeh(track, h_idx, max_frame, data)
   
print('Task finished ^___^)')