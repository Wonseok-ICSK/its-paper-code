# Plot selected vehicle trajectories from recording CSV data.
# Input/output paths and recording selections are local research settings.
##
# ID를 입력하면 해당 ID를 그려주는 코드
##

import matplotlib.pyplot as plt
import csv

tracks = [11,12,13,14
,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

FRAME = 0
ID = 1
X_POS = 2
X_SPD = 6
LANE = 24

FPS = 25

def drawTrajectory(filename, lane, idx): # idx가 list로 들어왔을 때, 어떻게 할지 생각해보기.
  isExist = False
  with open(filename, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)
    max_spd = 0
    min_spd = 100
    idx_length = len(idx)
    
    x_values = [[] for i in range(idx_length)] # idx 만큼 크기의 2차원 리스트 생성
    y_values = [[] for i in range(idx_length)]
    z_values = [[] for i in range(idx_length)]

    #print(filename)
    #print(f'data lane {lane}, idx {idx}')

    for row in data:
      if row[LANE] == lane: #해당 차선에 대하여
        cur_idx = row[ID]
        for i in range(idx_length):
          if cur_idx == str(idx[i]):
            isExist = True
            spd = abs(float(row[X_SPD]))
            max_spd = max(max_spd, spd)
            min_spd = min(min_spd, spd)

            x_values[i].append(int(row[FRAME]) / FPS)
            y_values[i].append(float(row[X_POS]))
            z_values[i].append(abs(float(row[X_SPD])))

    if not isExist: # 찾은거 없으면 취소
      print('there is no data')
      return
    
    ## init plt        
    plt.figure(figsize=(55, 14), dpi=250)
    plt.rcParams.update({'font.size' : 22})
    plt.xlabel('second')
    plt.ylabel('distance x')        
    plt.set_cmap('gist_rainbow')
    plt.xlim(0, 800)
    plt.ylim(-50 , 450)
    
    for i in range(idx_length):
      plt.scatter(x_values[i], y_values[i], c=z_values[i], s=1, vmin=0, vmax=60) 

    plt.savefig('newSTD/a_temp_lane' + str(lane) + '_idx' + '.png')
    
    plt.colorbar()
    plt.show()

    print('process complete.')
    plt.close()


#### MAIN ####

for idx in tracks: # tracks open
  max_idx = 0
  file_name = '../data/' + str(idx) + '_tracks.csv' #
  
###
  u_idx = [i for i in range(53,150)]
  
  print(f'track {idx} input lane and id')
  u_lane = input()
  
  drawTrajectory(file_name, u_lane, u_idx)

  print('Paused, press any key to continue')
  input()

####
"""
  with open(file_name, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
      t_idx = int(row[ID])
      max_idx = max(max_idx, t_idx)

  sample = [[]for i in range(max_idx)]

  print('init complete.')
  
  for N_LANE in range(1, 8): # LANE
    max_frame = 0

    max_spd = 0.0
    min_spd = 100.0
    print(f'now processing TRACK {idx}  LANE {N_LANE}')

    plt.figure(figsize=(55, 14), dpi=250)
    plt.xlabel('second')
    plt.ylabel('distance x')

    with open(file_name, newline='') as csvfile:
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
      print('data is empty, file not saved')
      continue

    print(f'{max_spd}, {min_spd}')
    norm = plt.Normalize(min_spd, max_spd)
#    plt.clim(min_spd, max_spd)
    plt.set_cmap('gist_rainbow')

    print('data extract complete.')

    for i in range(max_idx): 
      if not sample[i]: # 해당 id가 없으면 생략
        continue

      x_values = [int(item[0]) / FPS for item in sample[i]] # frame
      y_values = [float(item[1]) for item in sample[i]] # x_pos
      z_values = [item[2] for item in sample[i]] # x_spd

      plt.scatter(x_values, y_values, c=z_values, s=1, vmin=min_spd, vmax=max_spd) 

      print(i)
      x_values.clear()
      y_values.clear()
      z_values.clear()

    plt.xlim(0, max_frame/25)
    plt.ylim(-50 , 450)

    print('process complete.')
    plt.colorbar()
    plt.savefig('newSTD/Track' + str(idx) + '_lane'+ str(N_LANE) +'.png')
    plt.close()
    sample = [[]for i in range(max_idx)]
    print('figure saved.')

print('task finished.')
"""