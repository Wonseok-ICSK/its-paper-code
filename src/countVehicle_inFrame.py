# 하나의 Frame에서 관측 가능한 차량의 수 count
# todo, 저속차량을 식별해서 count
# + ratio 도 같이 표시

import csv
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

TIMESTAMP = 25

for track in tqdm(tracks, desc='Progress '):
  max_idx = 0
  max_frame = -1

  tracks_csv = f'data/{track}_tracks.csv'
  tracksMeta_csv = f'data/{track}_tracksMeta.csv'

  with open(tracksMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
      max_frame = int(row[4])

  sec = 0
  count_vehicle = []
  
  df = pd.read_csv(tracks_csv)

  count_per_second = [df[df['frame'] == sec]['id'].nunique() for sec in range(0, max_frame + 1, TIMESTAMP)]

  plt.figure(figsize=(55, 14), dpi=250)
  plt.rcParams.update({'font.size' : 22})

  plt.title(f'Track {track} number of vehicle')
  plt.xlabel('Second')
  plt.ylabel('Vehicle')

  plt.xlim(0, max_frame/25)
  plt.ylim(0, max(count_per_second) + 10)

  #plt.bar(range(0, max_frame + 1, TIMESTAMP), count_per_second)
  plt.plot(count_per_second)

  plt.savefig(f'countvehicle/track{track}.png')