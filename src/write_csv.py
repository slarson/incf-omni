'''
Created on Dec 1, 2010

@author: slarson
'''
f = open('results.txt', 'r')
import pickle
distances_set = pickle.load(f)

import csv

#write out the raw distances for each distance comparisons
#one per row
writer = csv.writer(open('distances_set.csv', 'wb'), dialect='excel')
for distance_set in distances_set:
    writer.writerow(distance_set)

#write out the histogram for each distance comparison
import numpy as np    
writer2 = csv.writer(open('histogram_vals.csv', 'wb'), dialect='excel')
for distance_set in distances_set:
    #write a row with the values as the number
    # of points that fall into a 10 bin histogram
    writer2.writerow(np.histogram(distance_set)[0])