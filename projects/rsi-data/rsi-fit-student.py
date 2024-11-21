import pandas as pd
import numpy as np
from scipy.stats import norm, chisquare, ttest_ind, ttest_1samp
import matplotlib.pyplot as plt

"""
Preamble: Load data from source CSV file
"""
# load in the data
path = 'all_participant_data_rsi.csv'
data = np.loadtxt(path, delimiter=',', skiprows=1, usecols=[1,2,3])

# assign data columns
forceP_rsi = data[:,0]
accel_rsi = data[:,1]

"""
Question 1: Load the force plate and acceleration based RSI data for all participants. Map each data set (accel and FP)
to a normal distribution. Clearly report the distribution parameters (mu and std) and generate a graph two each curve's 
probability distribution function. Include appropriate labels, titles, and legends.
"""
print('-----Question 1-----')

# create sample normal distributions for both RSIs
xF = np.linspace(start=-3, stop=3, num=10000)

forceP_mu, forceP_std = norm.fit(forceP_rsi)
print(f"Force Plate RSI: Average = {forceP_mu:.4f}, Stdev = {forceP_std:.4f}")
forceP_sample = norm.pdf(xF, forceP_mu, forceP_std)
forceP_normal = norm.pdf(xF, 0, 1)

accel_mu, accel_std = norm.fit(accel_rsi)
print(f"Accelerometer RSI: Average = {accel_mu:.4f}, Stdev = {accel_std:.4f}")
accel_sample = norm.pdf(xF, accel_mu, accel_std)
accel_normal = norm.pdf(xF, 0, 1)

# plot each sample normal dist against the actual RSI dist
fig, axs = plt.subplots(1,2)

# plot force plate
axs[0].set_title('Force Plate RSI Mapped to Normal Distribution')
axs[0].plot(xF, forceP_sample, label=f"Data Fitted Normal\n(\u03BC = {forceP_mu:.2f}, STD = {forceP_std:.2f})",
            linewidth=2)

# plot accelerometer
axs[1].set_title('Accelerometer RSI Mapped to Normal Distribution')
axs[1].plot(xF, accel_sample, label=f"Data Fitted Normal\n(\u03BC = {accel_mu:.2f}, STD = {accel_std:.2f})",
            linewidth=2)

axs[0].legend()
axs[1].legend()
plt.tight_layout()
plt.show()

"""
Question 2: Conduct a Chi2 Goodness of Fit Test for each dataset to test whether the data is a good fit
for the derived normal distribution. Clearly print out the p-value, chi2 stat, and an indication of whether it is 
a fit or not. Do this for both acceleration and force plate distributions. It is suggested to generate 9 bins between 
[0,2), with the 10th bin encompassing [2,inf). An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 2-----')

# create 10 bins (more bins = higher precision?)
bins = np.linspace(-2, 2, 9)
# add infinity onto either end of the bins
bins = np.r_[-np.inf, bins, np.inf]

"""
Acceleration
"""
# place observations into bins
observed_counts, observed_edges = np.histogram(accel_rsi, bins=bins, density=False)

# find probability of each bin
expected_prob = np.diff(norm.cdf(bins, loc=accel_mu, scale=accel_std))

# Expected frequency for each bin
expected_counts = expected_prob * len(accel_rsi)

# Conduct chi2 test
# Reduce the degrees of freedom as the normal distribution has two parameters
(chi_stat, p_value) = chisquare(f_obs=observed_counts, f_exp=expected_counts, ddof=1)
print(f"Accelerometer Chi2 Stat: {chi_stat:.4f}, Accelerometer P-Value: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print('Reject null hypothesis. Counts for accelerometer RSI are not equal.')
else:
    print('Accept null hypothesis. Counts for accelerometer RSI are equal')

"""
Force Plate
"""
# place observations into bins
observed_counts, observed_edges = np.histogram(forceP_rsi, bins=bins, density=False)

# find probability of each bin
expected_prob = np.diff(norm.cdf(bins, loc=forceP_mu, scale=forceP_std))

# Expected frequency for each bin
expected_counts = expected_prob * len(forceP_rsi)

# Conduct chi2 test
# Reduce the degrees of freedom as the normal distribution has two parameters
(chi_stat, p_value) = chisquare(f_obs=observed_counts, f_exp=expected_counts, ddof=2)
print(f"Force Plate Chi2 Stat: {chi_stat:.4f}, Force Plate P-Value: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print('Reject null hypothesis. Counts for force plate RSI are not equal.')
else:
    print('Accept null hypothesis. Counts for force plate RSI are equal')

"""
Question 3: Perform a t-test to determine whether the RSI means for the acceleration and force plate data are equivalent 
or not. Clearly report the p-value for the t-test and make a clear determination as to whether they are equal or not.
"""
print('\n\n-----Question 3-----')

samp_stat, p_value = ttest_ind(forceP_rsi, accel_rsi)
print(f"2-Sample Stat: {samp_stat:.4f}, 2-Sample P-Value: {p_value:.4f}")

if p_value < alpha:
    print('Reject null hypothesis. Force plate and accelerometer RSIs are not equivalent.')
else:
    print('Accept null hypothesis. Force plate and accelerometer RSIs are equivalent.')

"""
Question 4 (Bonus): Calculate the RSI Error for the dataset where error is expressed as the difference between the 
Force Plate RSI measurement and the Accelerometer RSI measurement. Fit this error distribution to a normal curve and 
plot a histogram of the data on the same plot showing the fitted normal curve. Include appropriate labels, titles, and 
legends. The default binning approach from matplot lib with 16 bins is sufficient.
"""
# calculate the error between force plate and accelerometer RSI
error = [forceP_rsi[i] - accel_rsi[i] for i in range(len(data))]

# calculate statistical stuff
error_mu, error_std = norm.fit(error)
x = np.linspace(min(error), max(error), num=100)
error_norm = norm.pdf(x, error_mu, error_std)

# plot
plt.title("Normally Fitted Error vs. Histogram Fitted Error")

plt.plot(x, error_norm, label="Normally Fitted Error", linewidth=2)
plt.hist(error, bins=24, density=True, edgecolor='k', label='Histogram Fitted Error')

plt.legend()
plt.show()
