#mmc with different values for service rates 
from scipy import mean, digitize, cumsum, array, concatenate, set_printoptions, nonzero, insert, ones, random
from scipy.stats import uniform, expon

import numpy as np
from QueueingTheory import mm1, getRandomArrivalServiceTimes
def prints(s):
    print s
    return s

set_printoptions(precision = 7)
set_printoptions(suppress=True)

arrival_rate = 1
service_rate = 1/6.0 * ones(3) #array([1.09, 2.000005, 1])
server_prob = array([0.25, 0.25, 0.5])
n_server = server_prob.size
n_process = 100
time_interval = 10

initial_state = (7,2,3)
arrival_times = getRandomArrivalServiceTimes(n_process, arrival_rate, None)[0]
sum_initial_state = sum(initial_state)
# preparing initial state for each mm1 simulation

initial_states = zip(initial_state, [arrival_times[sum_initial_state]] * len(initial_state))

# maps kth process to ith server
server_address_table_forced = random.permutation(concatenate([ones(state) * i for i,state in enumerate(initial_state)]))
print "forced server address table", server_address_table_forced
server_address_table = concatenate([server_address_table_forced, digitize(uniform.rvs(size = n_process-sum_initial_state), cumsum(server_prob))])
server_arrival_times = [arrival_times[server_address_table == i] for i in range(n_server)]
server_service_times = [
    getRandomArrivalServiceTimes((server_address_table == i).sum(), None, service_rate[i])[1]
    for i in range(n_server)
]

results = map(mm1, server_arrival_times, server_service_times, initial_states)
print "Mean QueueSize(1)", array([mean(result['queue_size']) for result in results])
print "Results[0]['queue_size']", results[0]['queue_size']
print "Results[1]['queue_size']", results[1]['queue_size']
print "Results[2]['queue_size']", results[2]['queue_size']
time_start = arrival_times[sum_initial_state] # I don't know why it shouldn't be sum_initial_state +1 instead
print "queue_size_by_time", time_start, [r['queue_size_by_time'](time_start) for r in results]
print "queue_size_by_time", time_start+time_interval, [r['queue_size_by_time'](time_start+time_interval) for r in results]
