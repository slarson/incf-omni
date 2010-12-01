'''
Created on Dec 1, 2010

@author: slarson
'''
f = open('results.txt', 'r')
import pickle
distances_set = pickle.load(f)

import csv

writer = csv.writer(open('distances_set.csv', 'wb'), dialect='excel')
for distance_set in distances_set:
    writer.writerow(distance_set)