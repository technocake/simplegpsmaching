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

@jit(nopython=True)
def equirectangular_distance_approximation(lat1, lon1, lat2, lon2):
    deglen = 110250.
    x = lat1 - lat2
    y = (lon1 - lon2)*math.cos(lat2)
    return deglen*math.sqrt(x*x + y*y)


@njit
def find(table, radius=50):
    # Get trajectories of first user
    mark = np.zeros((table.shape[1]))
    suspected = 0
    for x in range(table.shape[0]):  # timesteps
        for y in range(table.shape[1]):  # users
            if y > 0:

                # Skip if user is missing GPS data 
                if table[x,y,0] == 0:
                    mark[y] = 0
                    continue

                # Compute distance
                dist = haversine(table[x,y,0], table[x,y,1], table[x,0,0], table[x,0,1])
                
                # Mark as infected
                if dist < radius:
                    if mark[y]==1:
                        print("Trace ",y," overlaps with infected at Long / Lat: ",table[x,y,0],table[x,y,1])
                        suspected += 1
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
