import scipy
import random
from scipy.stats import expon
from scipy import mean, cumsum
arrival_rate = 1 / 40.0
n_process = 1000
sum_list = []
variance_list = []
for j in range(5):
    time_intervals = expon.rvs(scale = 1/arrival_rate, size = n_process - 1)
    arrival_times = scipy.insert(cumsum(time_intervals), 0, 0)
    sum_list.append(arrival_times[len(arrival_times) - 1] / 1000)
print sum_list
mean_sum_list = mean(sum_list)
for j in range(5):
    variance_list.append((sum_list[j] - mean_sum_list)**2)
print mean(variance_list)
print variance_list

