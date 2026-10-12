# Aggregate per-frame lane occupancy by recording and direction.
# Input/output paths and recording selections are local research settings.
# import pandas as pd
# from tqdm import tqdm

# tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS
# upstream = [2, 3, 4]
# downstream = [6, 7, 8]
# traget = 15 * 60 * 25 # frame by 15min

# tempU = [[] for _ in range(6)]
# for track in range(1,61, 1):
#   if track < 10:
#     track = '0' + str(track)

#   info = pd.read_csv('../data/' + str(track) + '_recordingMeta.csv')

#   location = info['locationId'].iloc[0]
#   max_frame = info['duration'].iloc[0] * 25
#   ratio = traget / max_frame

#   nOfUpStream = info['numVehicles'].iloc[0]

#   tempU[location - 1].append(nOfUpStream * ratio)

# res = []
# for i in range(location):
#   res.append({'Track': track, 'location': i, 'Average Upstream Vehicles' : (sum(tempU[i]) / len(tempU[i]))})

# result_df = pd.DataFrame(res)
# # Save the result DataFrame to a CSV file
# result_df.to_csv('result_sum.csv', index=False)








import pandas as pd
from tqdm import tqdm

tracks = [11,12,13,14,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57] # TRACKS
upstream = [2, 3, 4]
downstream = [6, 7, 8]
traget = 15 * 60 * 25 # frame by 15min

tempU = [[] for _ in range(6)]
tempD = [[] for _ in range(6)]
for track in range(1,61, 1):
  if track < 10:
    track = '0' + str(track)

  data = pd.read_csv('../data/' + str(track) + '_tracks.csv')
  info = pd.read_csv('../data/' + str(track) + '_recordingMeta.csv')

  location = info['locationId'].iloc[0]
  max_frame = data['frame'].max()
  ratio = traget / max_frame
  nOfUpStream = data[(data['laneId'].isin(upstream))]['id'].nunique()
  nOfDownStream = data[(data['laneId'].isin(downstream))]['id'].nunique()

  tempU[location - 1].append(nOfUpStream * ratio)
  tempD[location - 1].append(nOfDownStream * ratio)

res = []
for i in range(location):
  res.append({'Track': track, 'location': i, 'Average Upstream Vehicles' : (sum(tempU[i]) / len(tempU[i])), 'Average Downstream Vehicles' : (sum(tempD[i]) / len(tempD[i]))})

result_df = pd.DataFrame(res)
# Save the result DataFrame to a CSV file
result_df.to_csv('result_r.csv', index=False)