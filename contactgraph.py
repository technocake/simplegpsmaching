import math
import numpy as np
from numba import jit, njit
import time 
#from scipy import sparse
import igraph
from random import *


def checkinfected(i,cg,infectlimit):
	infected = 0
	for j in cg.neighbors(i):
		edge = cg.get_eid(i,j,error=False)
		if edge>-1:
			if cg.es[edge]["contacts"]>0 and cg.es[edge]["time"] < infectlimit:
				print(j," was infected by ",i)
				infected = infected+1
	return infected


def checkinfectedsilent(i,cg,infectlimit):
	infected = 0
	for j in cg.neighbors(i):
		edge = cg.get_eid(i,j,error=False)
		if edge>-1:
			if cg.es[edge]["contacts"]>0 and cg.es[edge]["time"] < infectlimit:
				infected = infected+1
	return infected

def sampleinfections(people,runs,cg,infectlimit):
	average=0
	for x in range(runs):
		runaverage=0
		for y in range(people):
			runaverage+=checkinfectedsilent(randrange(cg.vcount()),cg,7200)
		average+=runaverage
	return average/runs

def countinfections(cg,infectlimit):
	average=0
	for x in range(cg.vcount()):
		average+=checkinfectedsilent(x,cg,7200)
	return average/cg.vcount()


cg = igraph.Graph()

cg = cg.Read_GraphMLz("contactgraph50.3.zip")

igraph.summary(cg)

t1 = time.time()
checkinfected(0,cg,7200)
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


