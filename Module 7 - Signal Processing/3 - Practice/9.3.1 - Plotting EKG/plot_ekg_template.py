
import matplotlib.pyplot as plt
import numpy as np

# import the CSV file using numpy
path = '../../../data/ekg/mitdb_201.csv'

# load data in matrix from CSV file; skip first two rows

### Your code here ###
data = np.loadtxt(path, delimiter=',', skiprows=2)
# save each vector as own variable

### Your code here ###
time = data[:,0]
v5 = data[:,1]
v2 = data[:,2]
# use matplot lib to generate a single

### Your code here ###
plt.plot(time, v5)
plt.show()

