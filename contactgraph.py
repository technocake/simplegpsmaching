import pandas as pd
import math
import numpy as np
from numba import jit, njit
import time 
#from scipy import sparse
import igraph

@jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    R = 6372800  # Earth radius in meters

    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


def checkcontact(i,j,rowlist,cg,row):
	dist = haversine(rowlist[j][0],rowlist[j][1],rowlist[i][0],rowlist[i][1])
	if dist < 5:
		u = rowlist[i][2]
		v = rowlist[j][2]
		edge = cg.get_eid(u,v,error=False)
		if edge==-1:
			cg.add_edge(u,v)
			edge=cg.get_eid(u,v,error=False)
		cg.es[edge]["time"]=row;


def processrow(table,row,contactgraph):
	rowlist=[]
	for i in range(table.shape[1]):
		if table[row,i,0] > 0:
			item=(table[row,i,1],table[row,i,0],i)
			rowlist.append(item)
	rowlist.sort()
	for j in range(len(rowlist)):
		#west
		i = j-1
		while i>-1 and rowlist[j][0]-rowlist[i][0] < 0.00015:
			checkcontact(i,j,rowlist,cg,row)
			i=i-1
		#east
		i = j+1		
		while i<len(rowlist) and rowlist[i][0]-rowlist[j][0] < 0.00015:
			checkcontact(i,j,rowlist,cg,row)
			i=i+1



def checkinfected(i,cg,infectlimit):
	infected = 0
	for j in cg.neighbors(i):
		edge = cg.get_eid(i,j)
		if cg.es[edge]["time"] < infectlimit:
			print(j," was infected by ",i)
			infected = infected+1
	return infected


print("Loading matrix.npy")
table = np.load("matrix.npy")


cg = igraph.Graph()
cg.add_vertices(table.shape[1])

processrow(table,0,cg)



print("Building Graph")
t1 = time.time()
for x in range(table.shape[0]):
	processrow(table,x,cg)
print("Time: ",time.time()-t1)


checkinfected(10000,cg,7200)

