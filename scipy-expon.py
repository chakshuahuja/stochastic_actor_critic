from scipy.stats import expon
from scipy import mean
from time import time

t1 = time()
lambd = 0.1
expon_dist = expon(scale = 1.0/lambd)
dist = expon_dist.rvs(10000)

x = 15
# this is basically 1 - cdf or survival function sf
dist_more_x = dist[dist > x] 

formulated_sf = expon_dist.sf(x)
calculated_sf = len(dist_more_x)/float(len(dist))
formulated_mean = expon_dist.mean()
calculated_mean = mean(dist)
print "Time taken", time() - t1

print "Formulated Survival Function", formulated_sf
print "Calculated Survival Function", calculated_sf
print "Difference in Survival Function", formulated_sf - calculated_sf

print "Formulated Mean", formulated_mean
print "Calculatd Mean", calculated_mean
print "Difference in Mean", formulated_mean - calculated_mean

from matplotlib.pyplot import hist, plot, show
count, bins, ignored = hist(dist, bins=50, normed=True)
plot(bins, expon_dist.pdf(bins), 'k-', linewidth=2, color = 'r')
show()
