# Historical trajectory plotting experiment retained for comparison.
# Input/output paths and recording selections are local research settings.
"""
row 0 : frame(time)
row 1 : 차량 id
row 2 : 차량 x 좌표

frame info 25fps

track01_ 1048
track02_ 1113
track03_ 914
track0
track0
track0
track0
track0
track0
"""

import matplotlib.pyplot as plt
import csv

color = ['black', 'gray', 'lightcoral', 'red', 'brown', 'peru', 'darkorange', 'tan', 'gold', 'olive', 'yellow', 'lawngreen', 'honeydew', 'forestgreen', 'aquamarine', 'azure', 'teal', 'deepskyblue', 'dodgerblue', 'navy', 'slateblue', 'plum', 'violet', 'purple', 'pink']
colour = ['red', 'orangered', 'darkorange', 'orange', 'gold', 'limegreen', 'lime', 'dodgerblue', 'blue', 'navy', 'midnightblue']
colour5 = ['red', 'orange', 'yellow', 'lime', 'navy', 'black']

FRAME = 0
ID = 1
X_POS = 2
FPS = 25
LANE = 24
X_SPD = 6

N_LANE = 5
RANGE = 915

sample = [[]for i in range(RANGE)]

min_spd = float(200)
max_spd = float(0)


with open('../data/03_tracks.csv', newline='') as csvfile:
  next(csvfile)
  data = csv.reader(csvfile)
  for row in data:
    if int(row[LANE]) == N_LANE: # lane 5
      if int(row[FRAME]) >= 10000:
        continue
      #if int(row[FRAME]) > 5000:
        #continue
      cur_spd =  float(row[X_SPD])
      if cur_spd > max_spd:
        max_spd = cur_spd
      if cur_spd < min_spd:
        min_spd = cur_spd
      sample[int(row[ID]) - 1].append((row[FRAME], row[X_POS], cur_spd))

print('data extract complete.')

divider = float(max_spd - min_spd)

print('divider is', str(divider))

#for i in range(1048):
for i in range(RANGE): # id 1 ~ 400번까지만 표시할 것.
  if not sample[i]:
    continue

  #filtered_data = [(x, y) for x, y in sample if x < 500]
  x_values = [int(item[0]) for item in sample[i]] # frame
  y_values = [float(item[1]) for item in sample[i]] # x_pos
  z_values = [int(((item[2]) - min_spd) * 6 / divider) for item in sample[i]] # x_spd

  print(i)
  for i in range(len(x_values)):
    plt.scatter(x_values[i], y_values[i], s=1, color = colour5[z_values[i]%6])

 # if float()
  #plt.plot(x_values, y_values, linestyle='-')
  #plt.plot(x_values, y_values)
  #plt.scatter(x_values, y_values, s = 1, color=color[i%24])

plt.xlabel('frame')
plt.ylabel('distance x')

plt.show()

plt.savefig('Figure1.png', dpi=200, bbox_inches='tight')



"""
row 0 : frame(time)
row 1 : 차량 id
row 2 : 차량 x 좌표

frame info 25fps

import matplotlib.pyplot as plt
import csv

from pprint import pprint

color = ['black', 'gray', 'lightcoral', 'red', 'brown', 'peru', 'darkorange', 'tan', 'gold', 'olive', 'yellow', 'lawngreen', 'honeydew', 'forestgreen', 'aquamarine', 'azure', 'teal', 'deepskyblue', 'dodgerblue', 'navy', 'slateblue', 'plum', 'violet', 'purple', 'pink']
colour = ['red', 'orangered', 'darkorange', 'orange', 'gold', 'limegreen', 'lime', 'dodgerblue', 'blue', 'navy', 'midnightblue']

FRAME = 0
ID = 1
X_POS = 2
FPS = 25
LANE = 24
X_SPD = 6

N_LANE = 5

sample = [[]for i in range(1048)]

with open('../data/01_tracks.csv', newline='') as csvfile:
  next(csvfile)
  data = csv.reader(csvfile)
  for row in data:
    
    if int(row[LANE]) == N_LANE: # lane 5
      
      if int(row[FRAME]) > 5000:
        continue
      sample[int(row[ID]) - 1].append((row[FRAME], row[X_POS], int((float(row[X_SPD]) - 20) / 3.1)))

#pprint(sample, indent=4, width = 20)
print('data extract complete.')

#for i in range(1048):
for i in range(400): # id 1 ~ 400번까지만 표시할 것.
  if not sample[i]:
    continue
    
  #filtered_data = [(x, y) for x, y in sample if x < 500]
  x_values = [int(item[0]) for item in sample[i]] # frame
  y_values = [float(item[1]) for item in sample[i]] # x_pos
  z_values = [int(item[2]) for item in sample[i]] # x_spd

  for i in range(len(x_values)):
    plt.scatter(x_values[i], y_values[i], s=1, color = colour[z_values[i]])

 # if float()
  #plt.plot(x_values, y_values, linestyle='-')
  #plt.plot(x_values, y_values)
  #plt.scatter(x_values, y_values, s = 1, color=color[i%24])

plt.xlabel('frame')
plt.ylabel('distance x')

#plt.figure(figsize=(10, 6), dpi=200)
#plt.savefig('highD', dpi = 200)
plt.show()

"""