import matplotlib.pyplot as plt
import csv

colour5 = ['darkred', 'red', 'orange', 'yellow', 'lime', 'aqua', 'dodgerblue', 'blue', 'midnightblue', 'k', 'k', 'k']
            # 0-8    9-17     18-26     27-35    36-44    45-53   54-62         63-71   72-80           80+
            # 0      1        2         3        4        5       6             7       8               9

FRAME = 0
ID = 1
X_POS = 2
X_SPD = 6
LANE = 24

#초당 25프레임의 비디오
FPS = 25

max_idx = 0

lSensorA = [] # 100
locA = 100
lSensorB = [] # 200
lacB = 200
lSensorC = [] # 300
locC = 300


for idx in range(3, 6): # tracks_03 to tracks_05
  file_name = '../data/0' + str(idx) + '_tracks.csv' #
  with open(file_name, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)
    for row in data:
      if max_idx < int(row[ID]):
        max_idx = int(row[ID])

    print('max_idx calc complete')

  sample = [[]for i in range(max_idx)]
  
  for N_LANE in range(5, 7): # LANE
    saver = False
    print('now processing LANE ', str(N_LANE))

    plt.figure(figsize=(55, 14), dpi=250)
    plt.xlabel('second')
    plt.ylabel('distance x')
    plt.colorbar()

    with open(file_name, newline='') as csvfile:
      next(csvfile)
      data = csv.reader(csvfile)
      for row in data:
        if int(row[LANE]) == N_LANE:
          saver = True
          sample[int(row[ID]) - 1].append((row[FRAME], row[X_POS], int(abs(float(row[X_SPD])) / 9)))

    print('data extract complete.')

    for i in range(max_idx): 
      if not sample[i]: # 해당 id가 없으면 생략
        continue

      x_values = [int(item[0]) / FPS for item in sample[i]] # frame
      y_values = [float(item[1]) for item in sample[i]] # x_pos
      z_values = [int(item[2]) for item in sample[i]] # x_spd

      colourmap = plt.get_cmap('hsv')

      print(i)
      for i in range(len(x_values)):
        colors = colourmap(z_values[i] / max(z_values))
        plt.scatter(x_values[i], y_values[i], s=1, color = colors)
        
    print('process complete.')
    #plt.show()
    if saver:
      plt.savefig('newSTD/N-Figure_track' + str(idx) + '_lane'+ str(N_LANE) +'_StratToEnd.png')
      print('figure saved')