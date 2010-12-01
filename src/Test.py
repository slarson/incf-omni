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
os.environ["CLASSPATH"] = classpath

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
# imported from bitbucket.org/zornslemon/jnumeric-ra
from Numeric import *  

def loadMorphology ( uri_string ):
    app = Application()
    #get factory for producing tangibles
    factory = app.getTangibleFactory()
    #load by uri
    nm = factory.createNeuronMorphology(uri_string)
    #get neuron as JUNG tree
    t = nm.asTree()
    return t

def loadTree( uri_string ):
    # get an instance of the Application object
    app = Application()
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
    #initialize a new NeuronMorphology to work with the data in the data wrapper
    nm = NeuronMorphology()
    #set the data wrapper
    nm.setDataWrapper(data_wrapper)
    #get the neuron back as a JUNG tree
    t = nm.asTree()
    return t

def getEndpoints( tree ):
    #walk along tree to find end points -- tree search
    #return results as a JNumeric matrix with columns
    # x y z and one row per endpoint
    endpoints = []
    for v in tree.getVertices():
        if tree.isLeaf(v):
            endpoints.append(v)
    
    array_list = []
    for v in endpoints:
        array_list.append(array([v.x, v.y, v.z]));
    
    matrix = []
    for a in array_list:
        matrix = concatenate((matrix, a), axis=0)
    
    matrix = reshape(matrix,[-1,3])
    return matrix

def get_distance( array1, array2 ):
    diff_array = array1 - array2
    squared = diff_array * diff_array
    return sum(squared)

def get_distance_matrix( matrix1, matrix2 ):
    distance_matrix = zeros([shape(matrix1)[0],shape(matrix2)[0]], typecode='D')
    i = 0
    for array1 in matrix1[:]:
        j = 0
        for array2 in matrix2[:]:
            num = get_distance(array(array1), array(array2))
            distance_matrix[i,j] = num
            j = j + 1
        i = i + 1
    return distance_matrix

#def apply_tangible_position_rotation ( endpoints, x_pos, y_pos, z_pos, x_rot, y_rot, z_rot, w_rot)
    #apply the position and rotation to the endpoints, translating and rotating them

    
t1 = loadTree ("http://data.wholebraincatalog.org/datawrappers/generic/o3x4d")
t2 = loadMorphology("http://data.wholebraincatalog.org/tangibles/cellinstances/Ba2_1")
#t2 = loadMorphology("http://data.wholebraincatalog.org/tangibles/cellinstances/6xqgx")
#t2 = loadTree("http://data.wholebraincatalog.org/datawrappers/generic/BasketCell")
#t2 = loadTree( "http://data.wholebraincatalog.org/datawrappers/generic/gm7h5" )

matrix1 = getEndpoints(t1)
matrix2 = getEndpoints(t2)

distance_matrix = get_distance_matrix(matrix1, matrix2)
for row in distance_matrix[:]:
    min_distance = sorted(row, key=lambda x: x.real)[0].real
    print min_distance

#endpoints1 = getEndpoints(cell_segments1)
#endpoints1 = apply_tangible_position_rotation(endpoints1, 0, 0, 0, 0, 0, 0, 1)
#endpoints2 = getEndpoints(cell_segments2)
#endpoints2 = apply_tangible_position_rotation(endpoints2, 0, 0, 0, 0, 0, 0, 1)


