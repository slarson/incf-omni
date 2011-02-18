'''
Originally reated on Nov 27, 2010
Modified into a general example on Feb 18, 2011

Export all non-endpoints from a set of neuron morphologies stored in the Whole Brain Catalog.  
Export these as x,y,z coordinates in a Python pickle file.  This is step one in a 
two step process to analyze the contents of a neuron morphology from the Whole Brain
Catalog.  Step 2 will be to import the Python pickle file with a pure Python script 
and work with it using NumPy and Matplotlib modules.

Run via Jython
@author: slarson
'''

#Import the Application object from WBC
from org.wholebrainproject.wbc.app import Application
#Import the MorphMLImporter object from WBC
from org.wholebrainproject.wbc.data.importer import MorphMLImporter
#Import the NeuronMorphology object from WBC
from org.wholebrainproject.wbc.tangible import NeuronMorphology
#jython arrays
from array import array

#get neuron as JUNG forest (http://j.mp/dQSoVe)
def loadMorphology ( uri_string ):
    app = Application()
    app.setServerLocation("http://data.wholebraincatalog.org");

    #get factory for producing tangibles
    factory = app.getTangibleFactory()

    #load by uri
    nm = factory.createNeuronMorphology(uri_string)

    #convert NeuronMorphology to JUNG forest
    t = nm.asForest()
    return t

#find internal points (non leaves or roots) -- tree search
#return results as an array with columns
# x y z and one row per internal
def getInternalPoints( forest ):
    intpoints = []
    for i, v in enumerate(forest.getVertices()):
        if (not forest.isLeaf(v)) and (not forest.isRoot(v)):
		 #skip 4 out of 5 points to conserve memory
            if (i % 5 == 0): 
                intpoints.append(v)
    
    array_list = []
    for v in intpoints:
        array_list.append(array('f',[v.x, v.y, v.z]));
    
    return array_list

'''
SCRIPT BEGINS HERE
'''

uri_strings = ["http://data.wholebraincatalog.org/tangibles/cellinstances/6xqgx",
               "http://data.wholebraincatalog.org/tangibles/cellinstances/Gr4_1128",
               "http://data.wholebraincatalog.org/tangibles/cellinstances/Gr4_1130"]

# load the neuron from the Whole Brain Catalog
# as a JUNG forest into the forests array
forests = []
for uri_string in uri_strings:
    forests.append(loadMorphology(uri_string))

# find the points on the neuron that are not end points, 
# which we refer to as internal points and get them as a list.
internal_points = []
for f in forests:
    internal_points.append(getInternalPoints(f))

#Write the points out as a python pickle file so further analysis 
#can take place outside of Jython.
import pickle
f = open('points.txt', 'w')
pickle.dump(internal_points, f)
f.close()

print "Wrote points.txt as a pickle file with contents of http://data.wholebraincatalog.org/tangibles/cellinstances/6xqgx, http://data.wholebraincatalog.org/tangibles/cellinstances/Gr4_1128, http://data.wholebraincatalog.org/tangibles/cellinstances/Gr4_1130"
