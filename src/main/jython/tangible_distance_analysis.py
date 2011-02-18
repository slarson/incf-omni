'''
Created on Nov 27, 2010

Calculate the distance matrix between a set of NeuronMorphology end points via WBC
tangible download

Run via Jython
@author: slarson

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
    
    app.setServerLocation("http://137.131.164.54:8182");
    #get factory for producing tangibles
    factory = app.getTangibleFactory()
    #load by uri
    nm = factory.createNeuronMorphology(uri_string)
    #get neuron as JUNG forest
    t = nm.asForest()
    return t


def getEndpoints( forest ):
    #find end points (either leaves or roots) -- tree search
    #return results as a JNumeric matrix with columns
    # x y z and one row per endpoint
    endpoints = []
    for v in forest.getVertices():
        if forest.isLeaf(v) or forest.isRoot(v):
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
    
def distance_between_endpoints( f1, f2 ):
    
    #get the end points for both matrices
    #where the matrix has 3 columns (x,y,z)
    # and # of rows equal to the number of endpoints per
    # forest
    matrix1 = getEndpoints(f1)
    matrix2 = getEndpoints(f2)
    
    #calculate a distance matrix between the sets of endpoints
    #where each row has the distances between a point in matrix1
    # and all points in matrix2
    distance_matrix = get_distance_matrix(matrix1, matrix2)
    
    #walk the distance matrix row by row, sort the row, and give the 
    # min distance as the first (smallest) item in that row
    min_distance = []
    for row in distance_matrix[:]:
        #sort the row.  
        #use special sort due to complex numbers
        #present in matrix.
        s = sorted(row, key=lambda x: x.real)[0].real
        min_distance.append(s)
        
    return min_distance

'''
http://data.wholebraincatalog.org/tangibles/cellinstances/yazvy -> 011810_4R_flipN
http://data.wholebraincatalog.org/tangibles/cellinstances/nvjem -> 060710_1L_N
http://data.wholebraincatalog.org/tangibles/cellinstances/tc1kk -> 080410_5L_N
http://data.wholebraincatalog.org/tangibles/cellinstances/94cmu -> 022510_1L_N
http://data.wholebraincatalog.org/tangibles/cellinstances/dpkg6 -> 053110_1R_flipN
http://data.wholebraincatalog.org/tangibles/cellinstances/pgo54 -> 060710_1Rflip_N
http://data.wholebraincatalog.org/tangibles/cellinstances/qjqcd -> 072010_1L_N
'''

''' --original set
uri_strings = ["http://137.131.164.54:8182/tangibles/cellinstances/yazvy",
"http://137.131.164.54:8182/tangibles/cellinstances/nvjem",
"http://137.131.164.54:8182/tangibles/cellinstances/tc1kk",
"http://137.131.164.54:8182/tangibles/cellinstances/94cmu",
"http://137.131.164.54:8182/tangibles/cellinstances/dpkg6",
"http://137.131.164.54:8182/tangibles/cellinstances/pgo54",
"http://137.131.164.54:8182/tangibles/cellinstances/qjqcd"]
'''
# control set
uri_strings = ["http://137.131.164.54:8182/tangibles/cellinstances/76ux2",
"http://137.131.164.54:8182/tangibles/cellinstances/94cmu",
"http://137.131.164.54:8182/tangibles/cellinstances/94cmu2",
"http://137.131.164.54:8182/tangibles/cellinstances/94cmu3"]

#download and convert all forests upfront 
# to avoid repetative network crunching
forests = []
for uri_string in uri_strings:
    forests.append(loadMorphology(uri_string))

# do complete pairwise endpoint distance analysis
min_distance_complete_set = []
for f1 in forests:
    for f2 in forests:
        min_distance_complete_set.append(distance_between_endpoints(f1, f2))

f = open('results.txt', 'w')

import pickle
pickle.dump(min_distance_complete_set, f)
f.close()
#t1 = loadMorphology("http://137.131.164.54:8182/tangibles/cellinstances/s1pdd")
#t1 = loadMorphology("http://137.131.164.54:8182/tangibles/cellinstances/s1pdd2")
#t2 = loadMorphology("http://137.131.164.54:8182/tangibles/cellinstances/uafys")
#t2 = loadMorphology("http://data.wholebraincatalog.org/tangibles/cellinstances/Ba2_1")
#t2 = loadMorphology("http://data.wholebraincatalog.org/tangibles/cellinstances/6xqgx")
#t2 = loadTree("http://data.wholebraincatalog.org/datawrappers/generic/BasketCell")
#t2 = loadTree( "http://data.wholebraincatalog.org/datawrappers/generic/gm7h5" )

