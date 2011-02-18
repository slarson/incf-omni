'''
Created on Dec 3, 2010

@author: slarson
'''
import numpy as np

def matrixify (array_list):
    matrix = []
    for a in array_list:
        matrix = np.concatenate((matrix, a), axis=0)
    
    matrix = np.reshape(matrix,[-1,3])
    return matrix

def get_distance( array1, array2 ):
    diff_array = array1 - array2
    squared = diff_array * diff_array
    return sum(squared)

def get_distance_matrix( matrix1, matrix2 ):
    distance_matrix = np.zeros([np.shape(matrix1)[0],np.shape(matrix2)[0]])
    #change this to matrix form
    i = 0
    for array1 in matrix1[:]:
        j = 0
        for array2 in matrix2[:]:
            num = get_distance(np.array(array1), np.array(array2))
            distance_matrix[i,j] = num
            j = j + 1
        i = i + 1
    return distance_matrix
    
def distance_between_intpoints( p1, p2 ):
    
    #get the end points for both matrices
    #where the matrix has 3 columns (x,y,z)
    # and # of rows equal to the number of internal points per
    # forest
    matrix1 = matrixify(p1)
    matrix2 = matrixify(p2)
    
    #calculate a distance matrix between the sets of internal points
    #where each row has the distances between a point in matrix1
    # and all points in matrix2
    distance_matrix = get_distance_matrix(matrix1, matrix2)
    
    ######################################################3
    #Should be able to convert the following to matrix form
    ####################################################
    
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


f = open('points.txt', 'r')
import pickle
points_set = pickle.load(f)

# do complete pairwise endpoint distance analysis
min_distance_complete_set = []
for p1 in points_set:
    for p2 in points_set:
        min_distance_complete_set.append(distance_between_intpoints(p1, p2))
        
# write out results
f = open('results.txt', 'w')
pickle.dump(min_distance_complete_set, f)
f.close()

print "Wrote distance analysis out as results.txt"