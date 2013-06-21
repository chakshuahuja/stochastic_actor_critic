from scipy import mean, digitize, cumsum, array, concatenate, sort, split, set_printoptions
from scipy.stats import uniform
from QueueingTheory import mm1, getRandomArrivalServiceTimes
# QueueingTheory Module available on https://gist.github.com/siddhant3s/5665696
set_printoptions(precision = 3)
arrival_rate = 1
service_rate = 4/3.0
n_process = 10000
arrival_times, service_times = getRandomArrivalServiceTimes(n_process, arrival_rate, service_rate)
server_prob = array([0.2, 0.2, 0.2, 0.2, 0.2])
n_server = server_prob.size
# maps kth process to ith server
server_address_table = digitize(uniform.rvs(size = n_process), cumsum(server_prob))
server_arrival_times = [arrival_times[server_address_table == i] for i in range(n_server)]
server_service_times = [service_times[server_address_table == i] for i in range(n_server)]
results = map(mm1, server_arrival_times, server_service_times)
print "Mean Wait(1)", array([mean(result['wait_times']) for result in results])
print "Mean QueueSize(1)", array([mean(result['queue_size']) for result in results])
server_prob_matrix = array([[ 0.2,  0.2,  0.2,  0.2,  0.2],
                            [ 0.2,  0.2,  0.2,  0.2,  0.2],
                            [ 0.2,  0.2,  0.2,  0.2,  0.2],
                            [ 0.2,  0.2,  0.2,  0.2,  0.2],
                            [ 0.2,  0.2,  0.2,  0.2,  0.2]])
server_prob_matrix_cumsumed = cumsum(server_prob_matrix, axis = 1)
server_address_tables = [
    digitize(uniform.rvs(size = len(server_arrival_times[i])), server_prob_matrix_cumsumed[i])
    for i in range(n_server)
]
server_arrival_times = [
    sort(concatenate([results[i]['completion_times'][server_address_tables[i] == k]
                      for i in range(n_server)])) 
    for k in range(n_server)
]
new_service_times = getRandomArrivalServiceTimes(n_process, arrival_rate, service_rate)[1]
server_service_times = split(new_service_times, cumsum([x.size for x in server_arrival_times]))[:-1]
results2 = map(mm1, server_arrival_times, server_service_times)
print "Mean Wait(2)", array([mean(result['wait_times']) for result in results2])
print "Mean QueueSize(2)", array([mean(result['queue_size']) for result in results2])
