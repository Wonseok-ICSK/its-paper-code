# Historical trajectory plotting variant using a discrete color map.
# Input/output paths and recording selections are local research settings.
import matplotlib.pyplot as plt
import csv
import json
import os
import numpy as np
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable


colour_map = plt.get_cmap('gist_rainbow')  # Choose your desired colormap here
norm = plt.Normalize(0, 5)  # Adjust the normalization range based on your X_SPD values

tracks = [3]

FRAME = 0
ID = 1
X_POS = 2
X_SPD = 6
LANE = 24

FPS = 25

max_idx = 0
max_frame = 0

for idx in tracks:
    file_name = '../data/0' + str(idx) + '_tracks.csv' #
    with open(file_name, newline='') as csvfile:
        next(csvfile)
        data = csv.reader(csvfile)
        for row in data:
            if max_idx < int(row[ID]):
                max_idx = int(row[ID])
            if max_frame < int(row[FRAME]):
                max_frame = int(row[FRAME])

    sample = [[]for i in range(max_idx)]
    
    print('init complete.')
    
    for N_LANE in range(2, 8): # LANE
        print('now processing TRACK ' + str(idx) + '  LANE ', str(N_LANE))

        plt.figure(figsize=(55, 14), dpi=250)
        plt.xlabel('second')
        plt.ylabel('distance x')

        with open(file_name, newline='') as csvfile:
            next(csvfile)
            data = csv.reader(csvfile)
            for row in data:
                if int(row[LANE]) == N_LANE: #해당 차선에 대하여
                    sample[int(row[ID]) - 1].append((row[FRAME], row[X_POS], int(abs(float(row[X_SPD])) / 9)))

        print('data saved.')

        for i in range(max_idx): 
            if not sample[i]: # 해당 id가 없으면 생략
                continue

            x_values = [int(item[0]) / FPS for item in sample[i]] # frame
            y_values = [float(item[1]) for item in sample[i]] # x_pos
            z_values = [int(item[2]) for item in sample[i]] # x_spd

            print(i)
            for i in range(len(x_values)):
                color = colour_map(norm(z_values[i]))  # Map X_SPD to a color
                plt.scatter(x_values[i], y_values[i], s=2, color=color)

        divider = make_axes_locatable(plt.gca())
        cax = divider.append_axes("right", size="5%", pad=0.05)
        
        # Create a ScalarMappable for the colorbar
        sm = plt.cm.ScalarMappable(cmap=colour_map, norm=norm)
        sm.set_array([])

        # Add a colorbar to the plot
        cbar = plt.colorbar(sm, cax=cax, label='X_SPD')  # Add a label for the colorbar

        print('process complete.')
        plt.savefig('newSTD/c-bar_track' + str(idx) + '_lane'+ str(N_LANE) +'.png')
        print('figure saved.')

print('task finished.')
