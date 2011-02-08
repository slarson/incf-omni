'''
Created on Dec 1, 2010

Plot results from tangible_distance_analysis.  Run with python

@author: slarson
'''
f = open('results.txt', 'r')
import pickle
distances_set = pickle.load(f)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

fig = plt.figure()

length = len(distances_set)
size = np.sqrt(length)
i = 0
for distances in distances_set:
    ax = fig.add_subplot(size,size,i+1)
     # the histogram of the data
    n, bins, patches = ax.hist(distances, 10, facecolor='green', alpha=0.75)
    
    #ax.set_xlabel('Smarts')
    #ax.set_ylabel('Probability')
    #ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    #ax.set_xlim(40, 160)
    #ax.set_ylim(0, 0.03)
    plt.xticks([])
    plt.yticks([])
    ax.grid(True)
    i = i + 1

plt.show()
