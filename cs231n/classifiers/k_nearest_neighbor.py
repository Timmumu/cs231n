from builtins import range
from builtins import object
import numpy as np
from past.builtins import xrange
import operator

class KNearestNeighbor(object):
    """ a kNN classifier with L2 distance """   # L2 Euclidean Distance, Lecture 2

    def __init__(self):
        pass

    def train(self, X, y):
        """
        Train the classifier. For k-nearest neighbors this is just
        memorizing the training data.

        Inputs:
        - X: A numpy array of shape (num_train, D) containing the training data
          consisting of num_train samples each of dimension D.
        - y: A numpy array of shape (N,) containing the training labels, where
             y[i] is the label for X[i].
        """
        self.X_train = X
        self.y_train = y

    def predict(self, X, k=1, num_loops=0):
        """
        Predict labels for test data using this classifier.

        Inputs:
        - X: A numpy array of shape (num_test, D) containing test data consisting
             of num_test samples each of dimension D.
        - k: The number of nearest neighbors that vote for the predicted labels.
        - num_loops: Determines which implementation to use to compute distances
          between training points and testing points.

        Returns:
        - y: A numpy array of shape (num_test,) containing predicted labels for the
          test data, where y[i] is the predicted label for the test point X[i].
        """
        if num_loops == 0:
            dists = self.compute_distances_no_loops(X)
        elif num_loops == 1:
            dists = self.compute_distances_one_loop(X)
        elif num_loops == 2:
            dists = self.compute_distances_two_loops(X)
        else:
            raise ValueError('Invalid value %d for num_loops' % num_loops)

        return self.predict_labels(dists, k=k)

    def compute_distances_two_loops(self, X):
        """
        Compute the distance between each test point in X and each training point
        in self.X_train using a nested loop over both the training data and the
        test data.

        Inputs:
        - X: A numpy array of shape (num_test, D) containing test data.

        Returns:
        - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
          is the Euclidean distance between the ith test point and the jth training
          point.
        """
        num_test = X.shape[0]                   # num_test = 500; X shape: 500 x 3072; X.shape[0] = 500
        num_train = self.X_train.shape[0]       # num_train = 5000; X = X_test; self. returns to the class's instance(object) so that to access object.X_train shape: (5000, 3072)
        dists = np.zeros((num_test, num_train)) # result in a [500 x 5000] matrix
        for i in range(num_test):
            for j in range(num_train):
                #####################################################################
                # TODO:                                                             #
                # Compute the l2 distance between the ith test point and the jth    #
                # training point, and store the result in dists[i, j]. You should   #
                # not use a loop over dimension, nor use np.linalg.norm().          #
                #####################################################################
                # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
                DiffMatrix = np.subtract(X[i, :], self.X_train[j, :])
                DiffMatrixSq = np.square(DiffMatrix)
                DiffMatrixSqSum = DiffMatrixSq.sum(axis=0)  # axis = 0: sum all columns
                dists[i, j] = np.sqrt(DiffMatrixSqSum)
                # pass
                # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        return dists

    def compute_distances_one_loop(self, X):
        """
        Compute the distance between each test point in X and each training point
        in self.X_train using a single loop over the test data.

        Input / Output: Same as compute_distances_two_loops
        """
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        for i in range(num_test):
            #######################################################################
            # TODO:                                                               #
            # Compute the L2 distance between the ith test point and all training #
            # points, and store the result in dists[i, :].                        #
            # Do not use np.linalg.norm().                                        #
            #######################################################################
            # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
            testSplice = X[[i]]
            testSplice = np.tile(testSplice,(self.X_train.shape[0],1))
            diff = ((testSplice -self.X_train)**2).sum(axis=1)
            dists[i,:] = np.sqrt(diff)
            # pass
            # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        return dists

    def compute_distances_no_loops(self, X):
        """
        Compute the distance between each test point in X and each training point
        in self.X_train using no explicit loops.

        Input / Output: Same as compute_distances_two_loops
        """
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        #########################################################################
        # TODO:                                                                 #
        # Compute the L2 distance between all test points and all training      #
        # points without using any explicit loops, and store the result in      #
        # dists.                                                                #
        #                                                                       #
        # You should implement this function using only basic array operations; #
        # in particular you should not use functions from scipy,                #
        # nor use np.linalg.norm().                                             #
        #                                                                       #
        # HINT: Try to formulate the L2 distance using matrix multiplication    #
        #       and two broadcast sums.                                         #
        #########################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        # pass
        A = np.sum(X**2,axis=1)
        A = A.reshape(num_test,1)
        B = np.sum(self.X_train**2, axis=1)                 # 500 x 1
        B = B.reshape(1, num_train)                         # 1 x 5000
        C = A + B                        # broadcast summation -> 500 x 5000
        D = np.dot(X, self.X_train.T)   # [500x3072] X [5000x3072].T->[500x5000] 
        dists = np.sqrt(C - 2*D)

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        return dists

    def predict_labels(self, dists, k=1):
        """
        Given a matrix of distances between test points and training points,
        predict a label for each test point.

        Inputs:
        - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
          gives the distance betwen the ith test point and the jth training point.

        Returns:
        - y: A numpy array of shape (num_test,) containing predicted labels for the
          test data, where y[i] is the predicted label for the test point X[i].
        """
        num_test = dists.shape[0]
        y_pred = np.zeros(num_test)
        
        for i in range(num_test):
            # A list of length k storing the labels of the k nearest neighbors to
            # the ith test point.
            #########################################################################
            # TODO:                                                                 #
            # Use the distance matrix to find the k nearest neighbors of the ith    #
            # testing point, and use self.y_train to find the labels of these       #
            # neighbors. Store these labels in closest_y.                           #
            # Hint: Look up the function numpy.argsort.                             #
            #########################################################################
            # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
            sortedDistIndicies = dists[i,:].argsort()               # dist.shape : 500 x 5000, sort row by row to get sortedDistIndicies 1 x 5000
            sortedDistIndicies = sortedDistIndicies.tolist()
            y_train = self.y_train.tolist()                         # label: y_train : {ndarray, (5000,)}, convert ndarray to list
            closest_y = {} 

            for j in range(k):
                voteIlabel = y_train[sortedDistIndicies[j]]
                closest_y[voteIlabel] = closest_y.get(voteIlabel, 0) + 1         # if found key "voteIlabel = Truck," return value of truck + 1; if not found, create {"truck": 1}
            # pass
            # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
            #########################################################################
            # TODO:                                                                 #
            # Now that you have found the labels of the k nearest neighbors, you    #
            # need to find the MOST COMMON LABEL in the list closest_y of labels.   #
            # Store this label in y_pred[i]. Break ties by choosing the smaller     #
            # label.                                                                #
            #########################################################################
            # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
            
            # sorting
            # operator.itemgetter(1), 通过给key第一个域（即dict中的value）来排序
            # revserse: sort from big to small
            sorted_closest_y = sorted(closest_y.items(), key=operator.itemgetter(1), reverse=True)     # returns a 2D list: [('Orange', 3), ('Apple', 2)]
            y_pred[i] = sorted_closest_y[0][0]               # return the 1st key's 1st element
            # pass

            # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        return y_pred
