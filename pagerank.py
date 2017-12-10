#!/usr/bin/python

 
from subprocess import Popen
from numpy import genfromtxt

import numpy as np
from scipy.sparse import csc_matrix

Process=Popen('./getdata.bash %s ' % ("matrix.csv"), shell=True)


my_data = genfromtxt('matrix.csv', delimiter=',', skip_header=0)



def pageRank(G, s, maxerr = .001):

    n = G.shape[0]

    # transform G into markov matrix M
    M = csc_matrix(G,dtype=np.float)
    rsums = np.array(M.sum(1))[:,0]
    ri, ci = M.nonzero()
    M.data /= rsums[ri]

    # bool array of sink states
    sink = rsums==0

    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)
    while np.sum(np.abs(r-ro)) > maxerr:
        ro = r.copy()
        # calculate each pagerank at a time
        for i in range(0,n):
            # inlinks of state i
            Ii = np.array(M[:,i].todense())[:,0]
            # account for sink states
            Si = sink / float(n)
            # account for teleportation to state i
            Ti = np.ones(n) / float(n)

            r[i] = ro.dot( Ii*s + Si*s + Ti*(1-s) )

    # return normalized pagerank
    return r/sum(r)



print pageRank(my_data,s=0.5)

