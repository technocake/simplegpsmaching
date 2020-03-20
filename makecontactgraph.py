import pandas as pd
import math
import numpy as np
from numba import jit, njit
import time 
#from scipy import sparse
import igraph
from random import *

@jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    R = 6372800  # Earth radius in meters

    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))



def checkcontact(i,j,rowlist,cg,row,radius=5,exposurelimit=1):
	dist = haversine(rowlist[j][0],rowlist[j][1],rowlist[i][0],rowlist[i][1])
	u = rowlist[i][2]
	v = rowlist[j][2]
	edge = cg.get_eid(u,v,error=False)
	if dist < radius:
		if edge==-1:
			cg.add_edge(u,v)
			edge=cg.get_eid(u,v)
			cg.es[edge]["exposure"]=1
			cg.es[edge]["contacts"]=0
			cg.es[edge]["time"]=row
		else:
			cg.es[edge]["exposure"]+=1
		if cg.es[edge]["exposure"] == exposurelimit:
			cg.es[edge]["time"]=row
			cg.es[edge]["contacts"]+=1
			cg.es[edge]["time"]=row
	else:
		if edge>-1:
			cg.es[edge]["exposure"]=0

def reset(i,cg):
	for j in cg.neighbors(i):
		edge = cg.get_eid(i,j,error=False)
		if edge>-1:
			cg.es[edge]["exposure"]=0

def processrow(table,row,contactgraph,radius,exposurelimit):
	rowlist=[]
	for i in range(table.shape[1]):
		if table[row,i,0] > 0:
			item=(table[row,i,1],table[row,i,0],i)
			rowlist.append(item)
		else:
			reset(i,cg)

	rowlist.sort()
	for j in range(len(rowlist)):
		#west
		detectrange = 0.00003*radius
		i = j-1
		while i>-1 and rowlist[j][0]-rowlist[i][0] < detectrange:
			#checkcontact_minute(i,j,rowlist,cg,row)
			checkcontact(i,j,rowlist,cg,row,radius,exposurelimit)
			#checkcontact_merge(i,j,rowlist,cg,row,table)
			i=i-1
		#east
		i = j+1		
		while i<len(rowlist) and rowlist[i][0]-rowlist[j][0] < detectrange:
			#checkcontact_minute(i,j,rowlist,cg,row)
			checkcontact(i,j,rowlist,cg,row,radius,exposurelimit)
			#checkcontact_merge(i,j,rowlist,cg,row,table)			
			i=i+1



print("Loading matrix.npy")
table = np.load("matrix.npy")

radius=50
exposurelimit=3                                                  

cg = igraph.Graph()

cg.add_vertices(table.shape[1])
print("Building Graph")
t1 = time.time()
for x in range(table.shape[0]):
	processrow(table,x,cg,radius,exposurelimit)
print("Time: ",time.time()-t1)
name = "contactgraph"+str(radius)+"."+str(exposurelimit)+".zip"
cg.write_graphmlz(name)

#cg = cg.Read_GraphMLz("contactgraph10.5.zip")

igraph.summary(cg)

