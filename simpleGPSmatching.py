import pandas as pd
import os
import math
import numpy as np



def haversine(lat1,lon1,lat2,lon2):
    R = 6372800  # Earth radius in meters

    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))



data_dir="Data/"

	#user_df_map = {}
timesteps = 300
traces = 0
table = np.zeros((timesteps, traces+1, 2))

	# Loop over all data subdirectories
for subdir, dirs, files in os.walk(data_dir):

	# Loop over all plt files
	for file in files:
		if not file.endswith(".plt"):
			continue

		# Convert plt files to pandas frame
		df = pd.read_csv(os.path.join(subdir, file), sep=',', 
			             skiprows=[0,1,2,3,4,5], usecols=[0,1,5,6],
			             names=["Longitude", "Latitude", "Date", "Time"], header=None)

		# Append trahectories to user

		for x in range(timesteps):
			if x < df.shape[0]:
				table[x,traces-1,0]=df.values[x,0]
				table[x,traces-1,1]=df.values[x,1]

		traces = traces + 1
		table.resize((timesteps, traces, 2))
		print(df.shape[0])
		# user = int(subdir[5:8])
		# if user in user_df_map:
		# 	user_df_map[user] = user_df_map[user].append(df, ignore_index=True)
		# else:
		# 	user_df_map[user] = df

traces = traces - 1
			

#table = load_trajectories()

# Get trajectories of first user

suspected=0
for y in range(traces):
	if y > 0:
		for x in range(timesteps):
			dist = haversine(table[x,y,0],table[x,y,1],table[x,0,0],table[x,0,1])
			if dist < 50 and table[x,y,0]!= 0 and table[x,0,0] != 0:
				print("Trace ",y," overlaps with infected at Long / Lat: ",table[x,y,0],table[x,y,1])
				suspected=suspected+1
  

print(timesteps, traces,suspected)





from IPython import embed; embed()
