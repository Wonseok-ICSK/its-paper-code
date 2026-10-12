# Plot speed distributions and car/truck comparisons for each recording.
# Input/output paths and recording selections are local research settings.
import csv
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS

CLASS = 6
MEAN_VEL = 11

for idx in tqdm(tracks, desc='Progress '):
#for idx in tracks:
  lane_data = [[] for _ in range(9)]

  recordingMeta_csv = 'data/' + str(idx) + '_tracksMeta.csv'

  with open(recordingMeta_csv, newline='') as csvfile:
    next(csvfile)
    data = csv.reader(csvfile)
      
    car = []
    truck = []

    for row in data:
      if row[CLASS] == "Car":
        car.append(float(row[MEAN_VEL]) * 3.6)
      elif row[CLASS] == 'Truck':
        truck.append(float(row[MEAN_VEL]) * 3.6)

    car = sorted(car)
    truck = sorted(truck)


    plt.figure(figsize=(20, 12), dpi=200)

#    plt.hist([car, truck], bins=10 ,label=['car', 'truck'], density=True)
    # Calculate normalized histograms
    bins = np.linspace(min(min(car), min(truck)), max(max(car), max(truck)), 26)
    hist_car, bins_car, _ = plt.hist(car, bins=bins, density=True, alpha=1, label='car')
    hist_truck, bins_truck, _ = plt.hist(truck, bins=bins, density=True, alpha=0.7, label='truck')

    # Combine probabilities to ensure the sum is 1
    combined_hist = hist_car + hist_truck
    combined_bins = bins_car  # Assuming bins are the same for car and truck
    plt.rcParams.update({'font.size' : 22})

    plt.legend()

    plt.xlabel('Speed (km/h)')

    plt.ylabel('Normalized Frequency')

    plt.title(f'speed Histogram for Track {idx} (car / truck)')

    plt.savefig(f'hist/b_ratio_track{str(idx)}.png')

    plt.close()
