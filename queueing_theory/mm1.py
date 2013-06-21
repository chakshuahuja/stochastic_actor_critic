from scipy import mean, all, argmax
from QueueingTheory import mm1, getRandomArrivalServiceTimes
arrival_rate = 1
service_rate = 4/3.0
n_process = 100
arrival_times, service_times = getRandomArrivalServiceTimes(n_process, arrival_rate, service_rate)
result = mm1(arrival_times, service_times)

rho = arrival_rate/service_rate
formulated_mean_service_size = rho
formulated_mean_system_size = rho/(1 - rho)
formulated_mean_queue_size = formulated_mean_system_size - formulated_mean_service_size

print "Formulated Mean System Size:", formulated_mean_system_size
print "Calculated System Size:", mean(result['system_size'])
print "Formulated Queue Size:", formulated_mean_queue_size
print "Calculated Queue Size", mean(result['queue_size'])

print "Wait times", result['wait_times']
print "Enter Service", result['enter_service_times']
print "Completion", result['completion_times']
print "Arrival", arrival_times
print "Service", service_times
print all([result['queue_size_by_time'](time) for time in arrival_times] == result['queue_size'])
print "Index of max queue size", argmax(result['queue_size']), result['queue_size'][argmax(result['queue_size'])]
print "Arrival Time at that index", arrival_times[argmax(result['queue_size'])]
print result['queue_size']
