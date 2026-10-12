import csv
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

output_csv = 'truckRatiobyLane.csv'
results = []

for track in tqdm(tracks, desc='Progress '):
  max_idx = 0

  tracks_csv = f'data/{track}_tracks.csv' 
  tracksMeta_csv = f'data/{track}_tracksMeta.csv' 

  truck_idx = []
  car_idx = []

  with open(tracksMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)

    for row in data:
      if row[6] == "Car":
        car_idx.append(int(row[0]))
      else:
        truck_idx.append(int(row[0]))

  df = pd.read_csv(tracks_csv)

  groupByLane = df.groupby('laneId')

  for lane, data in groupByLane:
    idx = set(data['id'])
    cars = set(id for id in car_idx if id in idx)
    trucks = set(id for id in truck_idx if id in idx)

    cars = list(cars)
    trucks = list(trucks)

    truck_ratio = len(trucks) / (len(cars) + len(trucks)) * 100
    truck_ratio = f"{truck_ratio:.2f}"
    
    results.append([track, lane, len(trucks), len(cars), truck_ratio])

# Create a DataFrame from the results
result_df = pd.DataFrame(results, columns=['TRACK', 'LANE', 'num_trucks', 'num_cars', 'truck_ratio'])

# Export the DataFrame to a new CSV file
result_df.to_csv(output_csv, index=False)