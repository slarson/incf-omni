'''
Created on Nov 27, 2010

@author: slarson
'''
# not sure if this is making any difference
import sys
sys.path.append('C:\\Users\\slarson\\workspace\\OMNI\\target\\dependency\\')
#print sys.path
my_classpath = open('classpath.txt')
classpath = my_classpath.read()
paths = classpath.split(';')
for path in paths:
    sys.path.append(path)
#print sys.path

# doesn't seem to make any difference
import os
os.putenv("CLASSPATH",classpath)
#print os.environ["CLASSPATH"]


'''
Desired algorithm:  Pull out two specific neuronal morphologies
For each morphology, get all the end points.  
For each endpoint, apply the position / rotation of the tangible. 
For each endpoint in one morphology, search to find the nearest 
end point in the other morphology via euclidian distance.  Store 
all distances in an array.  Compute the mean of this array.
'''
'''
Begin code doing actual work with WBC library
'''
from org.wholebrainproject.wbc.app import Application
from org.wholebrainproject.wbc.data.importer import MorphMLImporter
from org.wholebrainproject.wbc.tangible import NeuronMorphology

def loadDataWrapper( uri_string ):
    # get an instance of the Application object
    app = Application();
    # get the local data repository
    data_repo = app.getLocalDataRepository()
    #get the data wrapper
    data_wrapper = data_repo.getDataWrapper(uri_string)
    # look up a specific neuroML morphology data wrapper by its WBC ID
    cell_location = data_wrapper.getLocation()
    #get an appropriate importer for this type of data wrapper
    importer = MorphMLImporter(cell_location)
    #import the data
    data = importer.getData()
    #set the data back on the wrapper so it can be accessed easily
    data_wrapper.setDownloaded(data)
    return data_wrapper

#def getEndpoints( cell_segments ):
    #walk along segments to find end points -- tree search
    
#def apply_tangible_position_rotation ( endpoints, x_pos, y_pos, z_pos, x_rot, y_rot, z_rot, w_rot)
    #apply the position and rotation to the endpoints, translating and rotating them
    
#def calculateDistance( endpoints1 endpoints2 )
    # calculate n^2 distances between all end points
    # per end point, find nearest neighbor in other list
    # add distance to array
    # return average of this array.
    
data_wrapper = loadDataWrapper ("http://data.wholebraincatalog.org/datawrappers/generic/o3x4d")

#initialize a new NeuronMorphology to work with the data in the data wrapper
nm = NeuronMorphology();
#set the data wrapper
nm.setDataWrapper(data_wrapper);
#get the neuron back as a JUNG tree
t = nm.asTree();

endpoints = []
for v in t.getVertices():
    if t.isLeaf(v):
        endpoints.append(v)
        
print len(endpoints)
#endpoints1 = getEndpoints(cell_segments1)
#endpoints1 = apply_tangible_position_rotation(endpoints1, 0, 0, 0, 0, 0, 0, 1)
#endpoints2 = getEndpoints(cell_segments2)
#endpoints2 = apply_tangible_position_rotation(endpoints2, 0, 0, 0, 0, 0, 0, 1)

#avg_distance = calculateDistance(endpoints1, endpoints2)

#print out some coordinates from a segment
#print str(cell_segments1[0].getDistal().getX()) + ", " + str(cell_segments1[0].getProximal().getX())

# imported from bitbucket.org/zornslemon/jnumeric-ra
'''
from Numeric import *
x = array([[1,2,3],[4,5,6]])
print x.shape
y = array([[1,2],[3,4],[5,6]])
print y.shape
print dot(x,y)
'''
