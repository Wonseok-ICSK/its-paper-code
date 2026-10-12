# Plot trajectories with distinct styling for truck observations.
# Input/output paths and recording selections are local research settings.
# Truck의 색상을 달리한 Traj 생성

import matplotlib.pyplot as plt
import csv
from tqdm import tqdm

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

vehicle_map = {"Car" : 0, "Truck" : 1}

FRAME = 0
ID = 1
X_POS = 2
X_SPD = 6
LANE = 24

FPS = 25

for idx in tqdm(tracks, desc='Progress '):
  max_idx = 0

  tracks_csv = '../data/' + str(idx) + '_tracks.csv' # 
  recordingMeta_csv = '../data/' + str(idx) + '_recordingMeta.csv' # location, spdLimit, day, time, 
  tracksMeta_csv = '../data/' + str(idx) + '_tracksMeta.csv' # meanVel, 
  
  with open(recordingMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
      max_idx = int(row[10])

  vehicleInfo = []

  with open(tracksMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
      vehicleInfo.append(vehicle_map[row[6]])

  for N_LANE in range(2, 9): # LANE
    sample = [[]for i in range(max_idx)]

    max_frame = 0

    max_spd = 0.0
    min_spd = 100.0
    #print(f'now processing TRACK {idx}  LANE {N_LANE}')

    with open(tracks_csv, newline='') as csvfile:
      next(csvfile)
      data = csv.reader(csvfile)
      for row in data:
        if int(row[LANE]) == N_LANE: #해당 차선에 대하여
          spd = abs(float(row[X_SPD]))
          max_frame = max(max_frame, int(row[FRAME]))
          max_spd = max(max_spd, spd)
          min_spd = min(min_spd, spd)

          sample[int(row[ID]) - 1].append((row[FRAME], row[X_POS], abs(float(row[X_SPD])))) 

    if max_frame == 0:
      continue

    plt.figure(figsize=(55, 14), dpi=250)
    plt.rcParams.update({'font.size' : 22})
    plt.xlabel('second')
    plt.ylabel('distance x')

    #print(f'{max_spd}, {min_spd}')
    norm = plt.Normalize(min_spd, max_spd)
#    plt.clim(min_spd, max_spd)
    plt.set_cmap('gist_rainbow')

    #print('data extract complete.')

    for i in range(max_idx): 
      if not sample[i]: # 해당 id가 없으면 생략
        continue

      x_values = [int(item[0]) / FPS for item in sample[i]] # frame
      y_values = [float(item[1]) for item in sample[i]] # x_pos
      z_values = [float(item[2]) * 3.6 for item in sample[i]] # x_spd

      for i in range(len(z_values)):
        z_values[i] = min(140.0, z_values[i])

      if vehicleInfo[i] == 1:
        plt.scatter(x_values, y_values, c='black', s=1, vmin=0.0, vmax=140.0)
      else:
        plt.scatter(x_values, y_values, c=z_values, s=1, vmin=0.0, vmax=140.0)
      

      #print(i)
      x_values.clear()
      y_values.clear()
      z_values.clear()

    plt.xlim(0, max_frame/25)
    plt.ylim(-50 , 450)

    plt.title('TRACK ' + str(idx) + ' LANE' + str(N_LANE))
    #print('process complete.')
    plt.colorbar(aspect=70).set_label('Vehicle Speed(km/h)')
    plt.savefig('newSTD/Track' + str(idx) + '_lane'+ str(N_LANE) +'.png', bbox_inches='tight', pad_inches=0.7)
    plt.close()
    #print('figure saved.')

print('task finished.')
