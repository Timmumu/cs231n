# helps to  lower dimension of the multi-dimensional matrix;
#           store the matrix;
#           reload the matrix.

import numpy as np

# Generate some test data
data = np.arange(200).reshape((4,5,10))         # 4 group, 5 rows, 10 columns for each group

# Write the array to disk
with open('test.txt', 'w') as outfile:
    # I'm writing a header here just for the sake of readability; Any line starting with "#" will be ignored by numpy.loadtxt
    outfile.write('# Array shape: {0}\n'.format(data.shape))

    # Iterating through a ndimensional array produces slices along
    # the last axis. This is equivalent to data[i,:,:] in this case
    for data_slice in data:

        # The formatting string indicates that I'm writing out
        # the values in left-justified columns 7 characters in width
        # with 2 decimal places.
        np.savetxt(outfile, data_slice, fmt='%-7.2f')

        # Writing out a break to indicate different slices...
        outfile.write('# New slice (text following # will be ignored by np.loadtxt) \n')


SavedData = np.loadtxt('test.txt').reshape((4, 5, 10))

