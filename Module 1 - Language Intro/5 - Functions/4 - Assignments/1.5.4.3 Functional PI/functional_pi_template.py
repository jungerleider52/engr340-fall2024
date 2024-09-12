import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    a = 1
    b = 1 / (math.sqrt(2))
    t = 0.25
    p = 1

    # perform 10 iterations of this loop
    for i in range(1, 10):
        """
        Step 2: Update each variable based upon the algorithm. Take care to ensure
        the order of operations and dependencies among calculations is respected. You
        may wish to create new "temporary" variables to hold intermediate results
        """

        ### YOUR CODE HERE ###

        # assign new values
        a1 = (a + b) / 2
        b1 = math.sqrt(a * b)
        p1 = 2 * p
        t1 = t - (p * ((a1 - a) ** 2))

        # update variables
        a = a1
        b = b1
        t = t1
        p = p1

        # print out the current loop iteration. This is present to have something in the loop.
        print("Loop Iteration: ", i)

        pi_estimate = ((a + b) ** 2) / (4 * t)

    # change this so an actual value is returned
    return pi_estimate



desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
