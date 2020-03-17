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

def checkcontact_merge(i,j,rowlist,cg,row,table):
	u = rowlist[i][2]
	v = rowlist[j][2]	
	length1=0
	length2=0
	for x in range(4):
		length1+= haversine(table[row+x][u][0],rowlist[row+x][u][1],rowlist[row+x+1][u][0],rowlist[row+x+1][u][1])
		length2+= haversine(table[row+x][v][0],rowlist[row+x][v][1],rowlist[row+x+1][v][0],rowlist[row+x+1][v][1])
	xydist = np.zeros(5,5)
	for x in range(5):
		for y in range(5):	
			xydist[x][y] = haversine(rowlist[row+x][u][0],rowlist[row+x][u][1],rowlist[row+x][v][0],rowlist[row+x][v][1])
	Aij = np.zeros(5,5)
	Bij = np.zeros(5,5)
	for x in range(5):
		Aij[x,0]=length1+haversine(table[row][u][0],table[row][u][1],table[row+x][v][0],table[row+x][v][1])
		Bij[0,x]=length2+haversine(table[row+x][u][0],table[row+x][u][1],table[row][v][0],table[row][v][1])

	for x in range(4):
		for y in range(5):
			Aij[x+1,y]=min(Aij[y,x]+haversine(table[row+x][u][0],table[row+x][u][1],table[row+x+1][u][0],table[row+x+1][u][1],Bij[y,x]+haversine(table[row+y][v][0],table[row+y][v][1],table[row+x+1][u][0],table[row+x+1][u][1])
			Bij[x+1,y]=min(Aij[x,y]+haversine(table[row+y][v][0],table[row+y][v][1],table[row+x+1][u][0],table[row+x+1][u][1],Bij[x,y]+haversine(table[row+y-1][v][0],table[row+y-1][v][1],table[row+y][v][0],table[row+y][v][1])
	length12 = min(Aij[4,4],Bij[4,4])
	dist=(length12/(length1+length2))-1
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


def checkinfectedsilent(i,cg,infectlimit):
	infected = 0
	for j in cg.neighbors(i):
		edge = cg.get_eid(i,j)
		if cg.es[edge]["time"] < infectlimit:
			infected = infected+1
	return infected

def sampleinfections(people,runs,cg,infectlimit):
	average=0
	for x in range(runs):
		runaverage=0
		for y in range(people):
			runaverage+=checkinfectedsilent(randrange(cg.ecount()),cg,7200)
		average+=runaverage
	return average/runs

def countinfections(cg,infectlimit):
	average=0
	for x in range(cg.vcount()):
		average+=checkinfectedsilent(x,cg,7200)
	return average/cg.vcount()

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

t1 = time.time()
checkinfected(10000,cg,7200)
print("Time: ",time.time()-t1)


people=1000
runs=1000

t1 = time.time()
s=sampleinfections(people,runs,cg,7200)
print ("Number of infections from ",people," infected at ",runs," runs:",s,"  (",s/people," per person)")
print("Time: ",time.time()-t1)

t1 = time.time()
print ("Average Number of infections from each individual:",countinfections(cg,7200))
print("Time: ",time.time()-t1)
