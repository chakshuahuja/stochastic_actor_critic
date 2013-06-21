import random
import math
from time import time
t1 = time()
lamb = 0.1
x = 15
li = []
for i in range(10000):
    li.append(random.expovariate(lamb))
req = []
for i in li:
    if i > x:
        req.append(i)
print "By formula : " + str(math.exp(-1 * lamb * x))
print "By manual calculation : " + str(len(req) / float(len(li)))
print "Error : " + str((math.exp(-1 * lamb * x)) - (len(req) / float(len(li))))
print "Actual Mean : " + str(sum(li) / float(len(li)))
print "Calculated Mean : " + str(1 / lamb)
print "time", time() - t1
