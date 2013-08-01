from scipy import mean, digitize, cumsum, array, concatenate, set_printoptions, nonzero, insert, ones, random, zeros, dot
from scipy.stats import expon, uniform
import numpy as np
from QueueingTheory import mm1, getRandomArrivalServiceTimes
from time import time
def prints(s):
    print s
    return s
set_printoptions(precision = 3)
set_printoptions(suppress = True)

arrival_rate = 1
#service_rate = 1/6.0 * ones(3)
service_rate = array([0.5, 0.1, 0.6])
server_prob = array([0.25, 0.5, 0.25])
n_server = server_prob.size 
n_process = 1000
time_interval = 10
max_no_people = 3
def state_number(state, max_n_process = max_no_people):
    return sum([state[i] * (max_n_process+1)**(len(states) -i -1) for i in range(len(state))])
    

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
    final_state =  [r['queue_size_by_time'](time_start+time_interval, max_no_people) if r else 0 for r in results] 
    return tuple(final_state)



iterations_for_each_state = 10
possible_states = [(i,j,k) for i in range(max_no_people+1) for j in range(max_no_people+1) for k in range(max_no_people+1)]
print "Possible States", len(possible_states)

initial_to_finals = {}
t0 = time()
from sys import stdout
BETA = 0.9
C = 0.1
B = 0.05

Q = dict(zip(possible_states, [zeros(n_server) for i in possible_states]))
Q1 = dict(zip(possible_states, [zeros(n_server) for i in possible_states]))
Pi = dict(zip(possible_states, [server_prob for i in possible_states]))
G = dict(zip(possible_states, [zeros(n_server) for i in possible_states]))
V =  dict(zip(possible_states, [dot(Pi[state], Q[state]) for state in possible_states]))

for k,state in enumerate(possible_states):
    initial_to_finals[state] = []
    for a in range(n_server):
        t1 = time()
        final_states =  [setUpNextState(state, Pi[state]) for i in range(iterations_for_each_state)]
        stdout.write(' '.join(['\r', "a=%i,State %i (of total %i) state: " % (a,k,len(possible_states)), str(state), str(time()- t1),str(time()-t0)]))
        stdout.flush()
        initial_to_finals[state].append(final_states)
        for final_state in final_states:
            Q[state][a] = sum(final_state) + BETA * V[final_state]
            G[state][a] = Q[state][a] - V[state]
            V[state] = V[state] + C * G[state][a]
        Pi[state][a] = max(0,Pi[state][a] + B * G[state][a] * (Pi[state][a] ** 0.5))
        Pi[state] = Pi[state]/float(Pi[state].sum())
#        print "Pi[state]_after", Pi[state]
            
# Q1min = array(Q1.values()).min(axis = 1)
# Q1argmin = array(Q1.values()).argmin(axis = 1)

print "Q Matrix:"
print array(Q.values())
# # print 
print "Pi Matrix:"
print array(Pi.values())
# # print 
# # print "G Matrix:"
# # print array(G.values())
# # print 
# print "V Array:", array(V.values())
# print "Q1min Array:", array(Q1min)
print "Pi.argmin", array(Pi.values()).argmax(axis = 1)

