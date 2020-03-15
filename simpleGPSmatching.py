import pandas as pd
import math
import numpy as np
from numba import jit, njit
import time 

@jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    R = 6372800  # Earth radius in meters

    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


@njit
def find(table, radius=50):
	# Get trajectories of first user
	mark = np.zeros((table.shape[1]))
	suspected = 0
	for x in range(table.shape[0]):
		for y in range(table.shape[1]):
			if y > 0:
				dist = haversine(table[x,y,0], table[x,y,1], table[x,0,0], table[x,0,1])
				if dist < radius and table[x,y,0] != 0 and table[x,0,0] != 0:
					if mark[y]==1:
						print("Trace ",y," overlaps with infected at Long / Lat: ",table[x,y,0],table[x,y,1])
						suspected = suspected+1
					else:
						mark[y] = 1
				else:
					mark[y] = 0
	print(table.shape[0], table.shape[1], suspected)


print("Loading matrix.npy")
table = np.load("matrix.npy")

print("Calling find")
t1 = time.time()
find(table)
print("Time: ",time.time()-t1)