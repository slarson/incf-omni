'''
Created on Nov 27, 2010

Export a set of NeuronMorphology *INTERNAL* points via WBC
tangible download

Run via Jython
@author: slarson

Begin code doing actual work with WBC library
'''
from org.wholebrainproject.wbc.app import Application
from org.wholebrainproject.wbc.data.importer import MorphMLImporter
from org.wholebrainproject.wbc.tangible import NeuronMorphology
from Numeric import *

def loadMorphology ( uri_string ):
    app = Application()
    
    app.setServerLocation("http://data.wholebraincatalog.org");
    #get factory for producing tangibles
    factory = app.getTangibleFactory()
    #load by uri
    nm = factory.createNeuronMorphology(uri_string)
    #get neuron as JUNG forest
    t = nm.asForest()
    return t


def getInternalPoints( forest ):
    #find internal points (non leaves or roots) -- tree search
    #return results as a JNumeric matrix with columns
    # x y z and one row per internal
    intpoints = []
    for i, v in enumerate(forest.getVertices()):
        if (not forest.isLeaf(v)) and (not forest.isRoot(v)):
            if (i % 5 == 0): #skip 4 out of 5 points to conserve memory
                intpoints.append(v)
    
    array_list = []
    for v in intpoints:
        array_list.append(array([v.x, v.y, v.z]));
    
    return array_list


'''
http://data.wholebraincatalog.org/tangibles/cellinstances/yazvy -> 011810_4R_flipN
http://data.wholebraincatalog.org/tangibles/cellinstances/nvjem -> 060710_1L_N
http://data.wholebraincatalog.org/tangibles/cellinstances/tc1kk -> 080410_5L_N
http://data.wholebraincatalog.org/tangibles/cellinstances/94cmu -> 022510_1L_N
http://data.wholebraincatalog.org/tangibles/cellinstances/dpkg6 -> 053110_1R_flipN
http://data.wholebraincatalog.org/tangibles/cellinstances/pgo54 -> 060710_1Rflip_N
http://data.wholebraincatalog.org/tangibles/cellinstances/qjqcd -> 072010_1L_N
'''
'''
uri_strings = ["http://137.131.164.54:8182/tangibles/cellinstances/yazvy",
"http://137.131.164.54:8182/tangibles/cellinstances/nvjem",
"http://137.131.164.54:8182/tangibles/cellinstances/tc1kk",
"http://137.131.164.54:8182/tangibles/cellinstances/94cmu",
"http://137.131.164.54:8182/tangibles/cellinstances/dpkg6",
"http://137.131.164.54:8182/tangibles/cellinstances/pgo54",
"http://137.131.164.54:8182/tangibles/cellinstances/qjqcd"]
'''
uri_strings = ["http://data.wholebraincatalog.org/tangibles/cellinstances/6xqgx"]

#download and convert all forests upfront 
# to avoid repetative network crunching
forests = []
for uri_string in uri_strings:
    forests.append(loadMorphology(uri_string))

internal_points = []
for f in forests:
    internal_points.append(getInternalPoints(f))

f = open('points.txt', 'w')

import pickle
pickle.dump(internal_points, f)
f.close()
#t1 = loadMorphology("http://137.131.164.54:8182/tangibles/cellinstances/s1pdd")
#t1 = loadMorphology("http://137.131.164.54:8182/tangibles/cellinstances/s1pdd2")
#t2 = loadMorphology("http://137.131.164.54:8182/tangibles/cellinstances/uafys")
#t2 = loadMorphology("http://data.wholebraincatalog.org/tangibles/cellinstances/Ba2_1")
#t2 = loadMorphology("http://data.wholebraincatalog.org/tangibles/cellinstances/6xqgx")
#t2 = loadTree("http://data.wholebraincatalog.org/datawrappers/generic/BasketCell")
#t2 = loadTree( "http://data.wholebraincatalog.org/datawrappers/generic/gm7h5" )

