"""
Given two lists, use the standard deviation function from numpy to determine
which language has the largest standard deviation. Usage will be np.std()
https://numpy.org/doc/stable/reference/generated/numpy.std.html
"""
from sys import stdlib_module_names

"""
Dr. Forsyth's Code. Do Not Modify.
"""
# bring in randomness because we need it in our lives
import random
import numpy as np

# randomly sample a distribution between 20 and 100
random_length = int(random.uniform(20, 100))

# generate a random list of random length containing values up to 100
random_list_A = random.sample(range(100), random_length)

# generate a random list of random length containing values up to 100
random_list_B = random.sample(range(100), random_length)

# use the std() method from numpy to determine which list has the largest standard deviation

# set this variable equal to the list with the largest standard deviation
# do not modify this variable's name, you can/should adjust the contents ;)
# e.g. longest_list_is = myList

### YOUR CODE HERE

# find the stdev of each list
std_A = np.std(random_list_A)
std_B = np.std(random_list_B)

# see if stdev in list A is greater than B
if std_A > std_B:
    largest_std = std_A
    print("The largest stdev is list A, with a stdev of:", std_A)
    longest_list_is = random_list_A
# if not, then stdev_B > stdev_A
else:
    largest_std = std_B
    print("The largest stdev is list B, with a stdev of:", std_B)
    longest_list_is = random_list_B
