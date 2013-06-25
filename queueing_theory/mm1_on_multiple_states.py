from scipy import mean, digitize, cumsum, array, concatenate, set_printoptions, nonzero, insert, ones, random
from scipy.stats import expon, uniform
import numpy as np
from QueueingTheory import mm1, getRandomArrivalServiceTimes
from time import time
def prints(s):
    print s
    return s
set_printoptions(precision = 7)
set_printoptions(suppress = True)

arrival_rate = 1
#service_rate = 1/6.0 * ones(3)
service_rate = array([0.000005, 0.00006, 0.0000001])
server_prob = array([0.25, 0.25, 0.5])
n_server = server_prob.size 
n_process = 1000
time_interval = 10

def setUpNextState(initial_state, server_prob, n_process=n_process):
    sum_initial_state = sum(initial_state)
    arrival_times = getRandomArrivalServiceTimes(n_process, arrival_rate, None)[0]
    time_start = arrival_times[sum_initial_state]
    # next two lines optimizes to avoid the processing of whole queeue, instead only processes which are needed
    # are processed
    arrival_times = arrival_times[arrival_times <= (time_start+time_interval)]
    n_process= arrival_times.size

    initial_states = zip(initial_state, [arrival_times[sum_initial_state]] * len(initial_state))
    server_address_table_forced = random.permutation(concatenate([ones(state) * i for i,state in enumerate(initial_state)]))
    server_address_table = concatenate([server_address_table_forced, digitize(uniform.rvs(size = n_process- sum_initial_state), cumsum(server_prob))])
    server_arrival_times = [arrival_times[server_address_table == i] for i in range(n_server)]
    server_service_times = [getRandomArrivalServiceTimes((server_address_table == i).sum(), None, service_rate[i])[1] for i in range(n_server)]
    results = map(mm1, server_arrival_times, server_service_times, initial_states)
    final_state =  [r['queue_size_by_time'](time_start+time_interval) if r else 0 for r in results] 
    return final_state


max_no_people = 10
iterations_for_each_state = 10
possible_states = [(i,j,k) for i in range(max_no_people) for j in range(max_no_people) for k in range(max_no_people)]
print "Possible States", len(possible_states)

initial_to_finals = {}
t0 = time()
from sys import stdout
for k,state in enumerate(possible_states):
    t1 = time()
    states_for_each_possible_state =  [setUpNextState(state, server_prob) for i in range(iterations_for_each_state)]
    stdout.write(' '.join(['\r', "State %i (of total %i) state: " % (k,len(possible_states)), str(state), str(time()- t1),str(time()-t0)]))
    stdout.flush()
    initial_to_finals[state] = states_for_each_possible_state
    
#setUpNextState((0,0,1), server_prob)
