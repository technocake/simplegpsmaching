import pandas as pd
import os
import math
import numpy as np
from numba import jit
import time 
from fileread import load_trajectories,create_time_slots

#@jit(nopython=True)
def haversine(lat1,lon1,lat2,lon2):
    R = 6372800  # Earth radius in meters

    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

#@jit(nopython=True)
def find(traces,timesteps,table):
	# Get trajectories of first user
	mark = np.zeros((traces))
	suspected=0
	for x in range(timesteps):
		for y in range(traces):
			if y > 0:
				dist = haversine(table[x,y,0],table[x,y,1],table[x,0,0],table[x,0,1])
				if dist < 500 and table[x,y,0]!= 0 and table[x,0,0] != 0:
					if mark[y]==1:
						print("Trace ",y," overlaps with infected at Long / Lat: ",table[x,y,0],table[x,y,1])
						suspected=suspected+1
					else:
						mark[y]=1
				else:
					mark[y]=0
	print(timesteps, traces,suspected)



	#user_df_map = {}
timesteps = 7200
traces = 20000
table = np.zeros((timesteps, traces, 2))
currenttrace=0


trajectories = load_trajectories()
trajectories = create_time_slots(trajectories)

trajectories[]
for x in range():
	for x in range(df.shape[0]):
		timestep = t(x)
		if table[timestep,currenttrace,0]!=0:
			table[timestep,traces,0]=df.values[x,0]
			table[timestep,traces,1]=df.values[x,1]
	currenttrace = currenttrace + 1
	if currenttrace > traces:
		traces=traces+1
		table.resize((timesteps, traces, 2))



		#print(df.shape[0])
		# user = int(subdir[5:8])
		# if user in user_df_map:
		# 	user_df_map[user] = user_df_map[user].append(df, ignore_index=True)
		# else:
		# 	user_df_map[user] = df
			

#table = load_trajectories()
t1 = time.time()
find(traces,timesteps,table)
print("Time: ",time.time()-t1)



from IPython import embed; embed()
