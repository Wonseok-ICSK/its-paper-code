# Shared trajectory-analysis helpers for counts, delay, headway and slow vehicles.
# Frame indices and physical time must be distinguished by each caller.
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import integrate

TIMESTAMP = 25
WINDOWSIZE = 3 * 25 # 15sec

# 구간에서 관측되는 차량을 계산하고 그래프를 그리는 함수
def countVeh(track, slow_idx, max_frame, data:pd.DataFrame):
  seperate_by_lane = data.groupby('laneId')

  for lane, lane_data in seperate_by_lane:
    count_per_second = [lane_data[lane_data['frame'] == sec]['id'].nunique() for sec in range(0, max_frame + 1, TIMESTAMP)]
    slow_per_second = [lane_data[(lane_data['frame'] == sec) & (lane_data['id'].isin(slow_idx))]['id'].nunique() for sec in range(0, max_frame + 1, TIMESTAMP)]

    # 도화지 생성
    plt.figure(figsize=(55, 14), dpi=250)
    plt.rcParams.update({'font.size' : 22})
    plt.xlim(0, max_frame/25)
    plt.ylim(0, max(count_per_second) + 10)

    # 정보 입력
    plt.title(f'Track {track} Lane {lane} Vehicle Count per second')
    plt.xlabel('Second')
    plt.ylabel('Vehicle')

    # 그림 그리기
    plt.plot(count_per_second)
    plt.plot(slow_per_second, c='r')

    # 파일 저장
    plt.savefig(f'countvehicle/i_track{track}_lane{lane}.png')
    plt.close()

# 구간(Time)을 입력으로 하여 해당 구간의 차량 수를 반환하는 함수가 필요함
def countVehInTime(data:pd.DataFrame, startTime, endTime): # 해당 시간대의 차량 수를 반환
  count_per_second = data[(data['frame'] >= startTime) & (data['frame'] <= endTime)]['id'].nunique()
  
  return count_per_second

def countVehs(data:pd.DataFrame): # 총 차량의 수 반환
  return data['id'].nunique()

def avgTT(data:pd.DataFrame): # 평균 Travel Time을 구하는 함수
  pass # 

# 두 그래프 사이의 넓이를 계산하는 함수
def measureDelay(startTime, endTime, graphA, graphB):
  graphA_clipped = np.clip(graphA[startTime:endTime], 0, None)
  graphB_clipped = np.clip(graphB[startTime:endTime], 0, None)

  # Calculate the difference between the clipped graphs
  diff = graphA_clipped - graphB_clipped

  # Integrate the clipped difference using trapezoidal rule
  totalDelay = integrate.trapezoid(diff)

  return totalDelay

# 평균 지체를 계산하는 함수 (sec)
def averageDelay(data:pd.DataFrame, startTime, endTime, graphA, graphB):
  vehCount = countVehInTime(data, startTime, endTime)
  totalDelay = measureDelay(startTime, endTime, graphA, graphB)
  avgDelay = totalDelay / vehCount if vehCount > 0 else 0
  
  return avgDelay

def spaceHeadway(data: pd.DataFrame):
  groupById = data.groupby('id')

  avg_headway = []
  for _, group_data  in groupById:
    #group_data  = group_data [['id', 'frame', 'dhw']]
    #firstFrame = group_data ['frame'].iloc[0]
    #selectedFrames = group_data [(group_data ['frame'] >= firstFrame) & (group_data ['frame'] <= firstFrame + 150)]
    avg_headway.append(group_data['dhw'].mean())
  avg_headway = [value for value in avg_headway if value != 0]
  # filtered_list = [value for value in original_list if value != 0]
  avg_headway = np.array(avg_headway).mean()
  return avg_headway

def spaceHeadways(data: pd.DataFrame, startTime, endTime):
  data = data[(data['frame'] <= endTime) & (data['frame'] >= startTime)]
  groupById = data.groupby('id')

  avg_headway = []
  for _, group_data  in groupById:
    avg_headway.append(group_data['dhw'].mean())
  avg_headway = [value for value in avg_headway if value != 0]
  results = np.array(avg_headway).mean()
  return results

def timeHeadway(data: pd.DataFrame):
  groupById = data.groupby('id')

  avg_headway = []
  for _, group_data  in groupById:
    #group_data  = group_data [['id', 'frame', 'thw']]
    #firstFrame = group_data ['frame'].iloc[0]
    #selectedFrames = group_data [(group_data ['frame'] >= firstFrame) & (group_data ['frame'] <= firstFrame + 150)]
    avg_headway.append(group_data['thw'].mean())
  
  avg_headway = [value for value in avg_headway if value != 0]
  avg_headway = np.array(avg_headway).mean()
  return avg_headway
  
def timeHeadways(data: pd.DataFrame, startTime, endTime):
  data = data[(data['frame'] <= endTime) & (data['frame'] >= startTime)]
  groupById = data.groupby('id')

  avg_headway = []
  for _, group_data  in groupById:
    avg_headway.append(group_data['thw'].mean())
  
  avg_headway = [value for value in avg_headway if value != 0]
  results = np.array(avg_headway).mean()
  return results

def averageSpeed(data: pd.DataFrame, startTime, endTime):
  groupById = data.groupby('id')
  avgSpeed = np.array([abs(3.6 * group_data[(group_data['frame'] <= endTime) & (group_data['frame'] >= startTime)]['xVelocity']).mean() for _, group_data in groupById])
  avgSpeed = avgSpeed[~np.isnan(avgSpeed)]
  return avgSpeed.mean()

def averageSpeeds(data: pd.DataFrame):
  groupById = data.groupby('id')
  avgSpeed = np.array([abs(3.6 * group_data['xVelocity']).mean() for _, group_data in groupById]).mean()
  return avgSpeed

def detectSlowVehs(data: pd.DataFrame):
  selected_cols = ['id', 'frame', 'xVelocity', 'precedingId', 'rightPrecedingId', 'leftPrecedingId']
  selected_data = data[selected_cols].copy()

  # 속도 차이 계산
  selected_data['precedingSpeed'] = selected_data.groupby('precedingId')['xVelocity'].mean()
  selected_data['leftSpeed'] = selected_data.groupby('leftPrecedingId')['xVelocity'].mean()
  selected_data['rightSpeed'] = selected_data.groupby('rightPrecedingId')['xVelocity'].mean()

  selected_data['speed_ratio'] = selected_data['speed_diff'] = (selected_data['xVelocity'] - selected_data['precedingSpeed']) / selected_data['xVelocity']
  
  selected_data['side_speed_ratio_left'] = selected_data.apply(lambda row: (row['xVelocity'] - row['leftSpeed']) / row['xVelocity'] if row['leftPrecedingId'] != 0 and pd.notnull(row['leftSpeed']) else pd.NA, axis=1)
  selected_data['side_speed_ratio_right'] = selected_data.apply(lambda row: (row['xVelocity'] - row['rightSpeed']) / row['xVelocity'] if row['rightPrecedingId'] != 0 and pd.notnull(row['rightSpeed']) else pd.NA, axis=1)


  # 속도 차이가 일정 비율 이상인 차량 필터링
  slow_vehicles = selected_data['id'][
    (selected_data['speed_ratio'] > 0.1) &
    (
      (
        (selected_data['side_speed_ratio_left'].isna()) |
        (selected_data['side_speed_ratio_left'].notna() & (selected_data['side_speed_ratio_left'] > 0.1))
      ) &
      (
        (selected_data['side_speed_ratio_right'].isna()) |
        (selected_data['side_speed_ratio_right'].notna() & (selected_data['side_speed_ratio_right'] > 0.05))
      )
    )
  ].unique()
  return slow_vehicles.tolist()

def detectSlowVeh(data: pd.DataFrame):
  t_time = time.time()

  print('a')
  col_id = data['id'].tolist()
  max_idx = data['id'].nunique()
  prec_id = data['precedingId'].tolist()
  r_prec_id = data['rightPrecedingId'].tolist()
  l_prec_id = data['leftPrecedingId'].tolist()
  col_speed = data['xVelocity'].tolist()
  col_speed = [abs(x * 3.6) for x in col_speed]
  col_frame = data['frame'].tolist()

  print(f'b, elapsed time : {t_time - time.time()}')
  t_time = time.time()
  idx_dict = {}
  c_veh_spd = [[] for _ in range(max_idx)]
  p_veh_spd = [[] for _ in range(max_idx)]
  veh_spd_diff = [[] for _ in range(max_idx)]
  side_veh_spd_diff = [[] for _ in range(max_idx)]

  print(f'c, elapsed time : {t_time - time.time()}')
  t_time = time.time()
  for frame, id, p_id, spd, l_id, r_id in zip(col_frame, col_id, prec_id, col_speed, l_prec_id, r_prec_id):
    if id not in idx_dict:
      idx_dict[id] = len(idx_dict)
    
    idx = idx_dict[id]

    if p_id != 0:
      prec_data = data[data['id'] == p_id]
      prec_frame_data = prec_data[prec_data['frame'] == frame]
      if not prec_frame_data.empty:
        prec_spd = abs(prec_frame_data['xVelocity'].iloc[0] * 3.6)
        c_veh_spd[idx].append(spd)
        p_veh_spd[idx].append(prec_spd)
        veh_spd_diff[idx].append(prec_spd - spd)

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

  print(f'd, elapsed time : {t_time - time.time()}')
  t_time = time.time()
  for id, idx in idx_dict.items():
    if len(c_veh_spd[idx]) != 0 and len(p_veh_spd[idx]) != 0:
      mean_diff = sum(veh_spd_diff[idx]) / len(veh_spd_diff[idx])
      if len(side_veh_spd_diff[idx]) != 0:
        mean_s_diff = sum(side_veh_spd_diff[idx]) / len(side_veh_spd_diff[idx])
      else:
        mean_s_diff = -1
        
      mean_p_vel = sum(p_veh_spd[idx]) / len(p_veh_spd[idx])
      # A speed ratio is undefined for a stationary preceding vehicle.
      if mean_p_vel == 0:
        continue

      prec_spd_ratio = mean_diff / mean_p_vel
      side_spd_ratio = mean_s_diff / mean_p_vel if mean_s_diff != -1 else -1

      if mean_s_diff != -1:
          if prec_spd_ratio > 0.1 and side_spd_ratio > 0.05:
              h_idx.append(id)
      else:
          if prec_spd_ratio > 0.1:
              h_idx.append(id)
  
  print(f'e, elapsed time : {t_time - time.time()}')
  t_time = time.time()
  return h_idx

def detectSlowVehPandas(data: pd.DataFrame):
  # Extracting columns
  col_id = data['id']
  max_idx = col_id.nunique()
  # col_prec_id = data['precedingId']
  # col_r_prec_id = data['rightPrecedingId']
  # col_l_prec_id = data['leftPrecedingId']
  # col_speed = abs(data['xVelocity'] * 3.6)
  # col_frame = data['frame']

  # Create a dictionary to store indices
  idx_dict = {}
  c_veh_spd = [[] for _ in range(max_idx)]
  p_veh_spd = [[] for _ in range(max_idx)]
  veh_spd_diff = [[] for _ in range(max_idx)]
  side_veh_spd_diff = [[] for _ in range(max_idx)]

  # Iterate through rows using iterrows
  for _, row in data.iterrows():
    id, frame, p_id, spd, l_id, r_id = row['id'], row['frame'], row['precedingId'], row['xVelocity'], row['leftPrecedingId'], row['rightPrecedingId']

    if id not in idx_dict:
      idx_dict[id] = len(idx_dict)
    
    idx = idx_dict[id]

    if p_id != 0:
      # Filter the data for precedingId
      prec_frame_data = data[(data['id'] == p_id) & (data['frame'] == frame)]

      if not prec_frame_data.empty:
        prec_spd = abs(prec_frame_data['xVelocity'].iloc[0] * 3.6)
        c_veh_spd[idx].append(spd)
        p_veh_spd[idx].append(prec_spd)
        veh_spd_diff[idx].append(prec_spd - spd)

      # Filter the data for leftPrecedingId
      l_data_at_frame = data[(data['id'] == l_id) & (data['frame'] == frame)]
      if not l_data_at_frame.empty:
        l_spd = abs(l_data_at_frame['xVelocity'].iloc[0] * 3.6)
        side_veh_spd_diff[idx].append(l_spd - spd)

      # Filter the data for rightPrecedingId
      r_data_at_frame = data[(data['id'] == r_id) & (data['frame'] == frame)]
      if not r_data_at_frame.empty:
        r_spd = abs(r_data_at_frame['xVelocity'].iloc[0] * 3.6)
        side_veh_spd_diff[idx].append(r_spd - spd)

  h_idx = []

  for id, idx in idx_dict.items():
    if len(c_veh_spd[idx]) != 0 and len(p_veh_spd[idx]) != 0:
      mean_diff = sum(veh_spd_diff[idx]) / len(veh_spd_diff[idx])
      mean_s_diff = sum(side_veh_spd_diff[idx]) / len(side_veh_spd_diff[idx]) if len(side_veh_spd_diff[idx]) != 0 else -1
      mean_p_vel = sum(p_veh_spd[idx]) / len(p_veh_spd[idx])
      # A speed ratio is undefined for a stationary preceding vehicle.
      if mean_p_vel == 0:
        continue

      prec_spd_ratio = mean_diff / mean_p_vel
      side_spd_ratio = mean_s_diff / mean_p_vel if mean_s_diff != -1 else -1

      if mean_s_diff != -1:
        if prec_spd_ratio > 0.1 and side_spd_ratio > 0.05:
          h_idx.append(id)
      else:
        if prec_spd_ratio > 0.1:
          h_idx.append(id)

  return h_idx

def detectSlowVehNew(data: pd.DataFrame):
  groupByLane = data.groupby('laneId')

  for lane, lane_data in groupByLane:
    dataByFrame = lane_data.groupby('frame')

    for frame, frame_data in dataByFrame:
      speed = frame_data['xVelocity']
      
      for row in frame_data.iterrows():
        myId = row['id']
        precId = row['precedingId']
        if precId != 0:
          # 속도 비교
          if (speed[myId] / speed[precId]) < 0.9:


            pass

def toCsv(data: pd.DataFrame, isTruck: bool, leaderId: int, track: int, startFrame: int): # 6초 전후의 결과값만 보면 됨
  results = []
#  startTime = data['frame'].min()
  laneId = data['laneId'].iloc[0]
  direction = "Upstream" if laneId <= 4 else "Downstream"
  #endFrame = startFrame + WINDOWSIZE  

  selected_data = data[(data['id'] >= leaderId)]

  # Calc 50m
  data_50 = selected_data[(selected_data['x'] > 48) & (selected_data['x'] < 52)]
  
  startFrame = data_50['frame'].min()
  endFrame = startFrame + WINDOWSIZE
  avg_speed = averageSpeed(data_50, startFrame, endFrame)
  avg_space_headway = spaceHeadways(data_50, startFrame, endFrame)
  avg_time_headway = timeHeadways(data_50, startFrame, endFrame)
  count_per_hour = 3600 / avg_time_headway
  results.append({
    "Track": track,
    "Lane": laneId,
    "Direction": direction,
    "LeaderVehId": leaderId,
    "isTruck": isTruck, 
    "Distance(m)": 50,
    "AverageTimeHeadway(sec)": avg_time_headway,
    "AverageSpaceHeadway(m)": avg_space_headway,
    "AverageSpeed(km/h)": avg_speed,
    # "AverageDelay(sec)": avg_delay, # Avg delay가 관측이 안됨.
    "k(veh/hr/lane)" : count_per_hour,
  })

  # Calc 200m
  data_200 = selected_data[(selected_data['x'] > 198) & (selected_data['x'] < 202)]

  startFrame = data_200['frame'].min()
  endFrame = startFrame + WINDOWSIZE
  avg_speed = averageSpeed(data_200, startFrame, endFrame)
  avg_space_headway = spaceHeadways(data_200, startFrame, endFrame)
  avg_time_headway = timeHeadways(data_200, startFrame, endFrame)
  count_per_hour = 3600 / avg_time_headway
  results.append({
    "Track": None,
    "Lane": None,
    "Direction": None,
    "LeaderVehId": None,
    "isTruck": isTruck, 
    "Distance(m)": 200,
    "AverageTimeHeadway(sec)": avg_time_headway,
    "AverageSpaceHeadway(m)": avg_space_headway,
    "AverageSpeed(km/h)": avg_speed,
    # "AverageDelay(sec)": avg_delay, # Avg delay가 관측이 안됨.
    "k(veh/hr/lane)" : count_per_hour,
  })

  # Calc 350m
  data_350 = selected_data[(selected_data['x'] > 348) & (selected_data['x'] < 352)]

  startFrame = data_350['frame'].min()
  endFrame = startFrame + WINDOWSIZE
  avg_speed = averageSpeed(data_350, startFrame, endFrame)
  avg_space_headway = spaceHeadways(data_350, startFrame, endFrame)
  avg_time_headway = timeHeadways(data_350, startFrame, endFrame)
  count_per_hour = 3600 / avg_time_headway
  results.append({
    "Track": None,
    "Lane": None,
    "Direction": None,
    "LeaderVehId": None,
    "isTruck": isTruck,
    "Distance(m)": 350,
    "AverageTimeHeadway(sec)": avg_time_headway,
    "AverageSpaceHeadway(m)": avg_space_headway,
    "AverageSpeed(km/h)": avg_speed,
    # "AverageDelay(sec)": avg_delay, # Avg delay가 관측이 안됨.
    "k(veh/hr/lane)" : count_per_hour,
  })

  startFrame = selected_data['frame'].min()
  endFrame = startFrame + WINDOWSIZE
  avg_speed = averageSpeed(selected_data, startFrame, endFrame)
  avg_space_headway = spaceHeadways(selected_data, startFrame, endFrame)
  avg_time_headway = timeHeadways(selected_data, startFrame, endFrame)
  count_per_hour = 3600 / avg_time_headway
  results.append({
    "Track": None,
    "Lane": None,
    "Direction": None,
    "LeaderVehId": None,
    "isTruck": isTruck,
    "Distance(m)": 'total',
    "AverageTimeHeadway(sec)": avg_time_headway,
    "AverageSpaceHeadway(m)": avg_space_headway,
    "AverageSpeed(km/h)": avg_speed,
    # "AverageDelay(sec)": avg_delay, # Avg delay가 관측이 안됨.
    "k(veh/hr/lane)" : count_per_hour,
  })

  results_df = pd.DataFrame(results) # Data Frame으로 변환
  results_df.to_csv(f"chart/SLOW_total.csv", mode='a', index=False) # csv파일로 작성


  '''
  # graphA, _, graphC = makeGraph(selected_data, startFrame, endFrame)
  # avg_delay = averageDelay(selected_data, startFrame, endFrame, graphA, graphC)
  avg_speed = averageSpeed(selected_data, startFrame, endFrame)
  avg_space_headway = spaceHeadway(selected_data)
  avg_time_headway = timeHeadway(selected_data)
  count_per_hour = 3600 / avg_time_headway
  results.append({
    "Track": track,
    "Lane": laneId,
    "Direction": direction,
    "LeaderVehId": leaderId,
    "isTruck": isTruck, 
    # "Time(sec)": i,
    "AverageTimeHeadway(sec)": avg_time_headway,
    "AverageSpaceHeadway(m)": avg_space_headway,
    "AverageSpeed(km/h)": avg_speed,
    # "AverageDelay(sec)": avg_delay, # Avg delay가 관측이 안됨.
    "k(veh/hr/lane)" : count_per_hour,
  })
  '''
  '''
  # 지금 이 코드가 초 단위로 반복하는거.
  for i in range(3, 10, 3):
    endTime = startTime + i * TIMESTAMP
    selected_data = data[(data['frame'] >= startTime) & (data['frame'] <= endTime)]

    graphA, _, graphC = makeGraphs(selected_data)
    avg_delay = averageDelay(selected_data, startTime, endTime, graphA, graphC)
    avg_speed = averageSpeed(selected_data, startTime, endTime)
    avg_space_headway = spaceHeadway(selected_data)
    avg_time_headway = timeHeadway(selected_data)
    count_per_second = countVehs(selected_data) / i * 3600

    results.append({
      "Track": track,
      "Lane": laneId,
      "Direction": direction,
      "LeaderVehId": leaderId,
      "isSlow": isSlow, 
      "Time(sec)": i,
      "AverageTimeHeadway(sec)": avg_time_headway,
      "AverageSpaceHeadway(m)": avg_space_headway,
      "AverageSpeed(km/h)": avg_speed,
      "AverageDelay(sec)": avg_delay, # Avg delay가 관측이 안됨.
      "k(veh/hr/lane)" : count_per_second,
    })

  '''

# startTime과 endTime에서의 가상 검지기 결과를 반환.
def makeGraph(df: pd.DataFrame, startTime, endTime):
  threshold = 3

  df = df[(df['frame'] >= startTime) & (df['frame'] <= endTime)]

  detector_A = df[df['x'].between(40 - threshold, 50 + threshold)].drop_duplicates('id')
  detector_B = df[df['x'].between(200 - threshold, 200 + threshold)].drop_duplicates('id')
  detector_C = df[df['x'].between(350 - threshold, 350 + threshold)].drop_duplicates('id')

  print('AAAAAAA')
  print(detector_A['frame'].value_counts())
  for i in range(1, len(detector_A)):
    detector_A[i] += detector_A[i - 1]
    detector_B[i] += detector_B[i - 1]
    detector_C[i] += detector_C[i - 1]

  detector_A = detector_A[::125]
  detector_B = detector_B[::125]
  detector_C = detector_C[::125]

  return detector_A, detector_B, detector_C 

def makeGraphs(df: pd.DataFrame):
  threshold = 3

  detector_A = df[df['x'].between(40 - threshold, 50 + threshold)].drop_duplicates('id')
  detector_B = df[df['x'].between(200 - threshold, 200 + threshold)].drop_duplicates('id')
  detector_C = df[df['x'].between(350 - threshold, 350 + threshold)].drop_duplicates('id')

  detector_A = detector_A['frame'].value_counts().sort_index().cumsum()
  detector_B = detector_B['frame'].value_counts().sort_index().cumsum()
  detector_C = detector_C['frame'].value_counts().sort_index().cumsum()

  detector_A = detector_A[::125]
  detector_B = detector_B[::125]
  detector_C = detector_C[::125]

  return detector_A, detector_B, detector_C 

def getTruckIds(track):
  data = pd.read_csv('data/' + str(track) + '_tracksMeta.csv')

  truckIds = data[(data['class'] == 'Truck')]['id'].tolist()

  return truckIds





"""
병렬처리로 speed up에 대한 idea
from concurrent.futures import ProcessPoolExecutor

def calculate_avg_headway(group_data):
    group_data = group_data[['id', 'frame', 'dhw']].sort_values(by='frame')
    first_frame = group_data['frame'].iloc[0]
    selected_frames = group_data[(group_data['frame'] >= first_frame) & (group_data['frame'] <= first_frame + 150)]
    return np.mean(selected_frames['dhw'].values)

def timeHeadway(data: pd.DataFrame):
    group_by_id = data.groupby('id')

    avg_headway_list = []
    with ProcessPoolExecutor() as executor:
        avg_headway_list = list(executor.map(calculate_avg_headway, group_by_id))

    avg_headway = np.mean(avg_headway_list)
    return avg_headway

"""