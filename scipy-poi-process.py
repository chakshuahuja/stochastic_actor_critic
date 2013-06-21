from scipy.stats import expon
from numpy import histogram
from scipy import mean,insert,cumsum,var,arange
lambd = 1/40.0
n_process = 10000
time_intervals = expon.rvs(scale = 1/lambd, size = n_process - 1)
arrival_times = insert(cumsum(time_intervals), 0, 0)
print arrival_times
size_intervals = 50000
bins = arange(0, arrival_times[-1], size_intervals)
print "Intervals:", bins
n_process_per_interval, edges = histogram(arrival_times, bins = bins)
print n_process_per_interval
print "Mean of # of process per interval", mean(n_process_per_interval)
print "Std.Dev of process per interval", var(n_process_per_interval)**0.5
from matplotlib import pyplot
pyplot.hist(arrival_times, bins = bins)
pyplot.show()
