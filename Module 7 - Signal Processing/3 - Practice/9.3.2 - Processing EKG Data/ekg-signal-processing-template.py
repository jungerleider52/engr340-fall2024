import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sp

"""
Step 0: Select which database you wish to use.
"""

# database name
database_name = 'mitdb_201'

# path to ekg folder
path_to_folder = "../../../data/ekg/"

# select a signal file to run
signal_filepath = path_to_folder + database_name + ".csv"

"""
Step #1: load data in matrix from CSV file; skip first two rows. Call the data signal.
"""

signal = np.loadtxt(signal_filepath, delimiter=',', skiprows=2)
#time = signal[:,0]
signal = signal[:,1]
#v2 = signal[:,2]

"""
Step 2: (OPTIONAL) pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6). These may not be correctly in radians
"""
#data = sp.butter(data, fs=250, N=6)


"""
Step 3: Pass data through weighted differentiator
"""
signal_diff = np.diff(signal)
"""
Step 4: Square the results of the previous step
"""
signal_square = np.square(signal_diff)
"""
Step 5: Pass a moving filter over your data
"""
signal_convolve = np.convolve(signal_square, [1,1,1])

# make a plot of the results. Can change the plot() parameter below to show different intermediate signals
fig, axs = plt.subplots(2,2)

axs[0, 0].set_title('Raw V5 Signal')
axs[0, 0].plot(signal)

axs[0, 1].set_title('V5 After Differentiation')
axs[0, 1].plot(signal_diff)

axs[1, 0].set_title('V5 After Squaring')
axs[1, 0].plot(signal_square)

axs[1, 1].set_title('V5 After Convolution')
axs[1, 1].plot(signal_convolve)

plt.tight_layout()
plt.show()