from scipy.stats import  expon
from scipy import cumsum,maximum,empty,insert,zeros
def getRandomArrivalServiceTimes(n_process, arrival_rate, service_rate):
    arrival_times, service_times = None, None
    if arrival_rate:
        time_intervals = expon.rvs(scale = 1/arrival_rate, size = n_process - 1)
        arrival_times = insert(cumsum(time_intervals),  0, 0)
    if service_rate:
        service_times = expon.rvs(scale = 1/service_rate, size = n_process)
    return arrival_times, service_times

def mm1(arrival_times, service_times, initial_state = None):
    """
    Does mm1 queue simulation, supports forcing of an initial_state of the Queue size:
    arrival_times: array of arrival times of this server
    service_times: array of service times of this server
    initial_state: a tuple (forced_queue_size, at_what_time)
                   This will force the queue_size at that time.
    """
    if arrival_times.size == 0 or service_times.size == 0:
        return None
        
    n_process = arrival_times.size
    initial_state = initial_state or (0,arrival_times[0])
    completion_times = empty(n_process)
    enter_service_times = empty(n_process)
    completion_times[0] = initial_state[1] + service_times[0]
    enter_service_times[0] = initial_state[1]

    for k in xrange(1, n_process):
        enter_service_times[k] = maximum(completion_times[k-1], arrival_times[k]) \
                                 if k > initial_state[0] else completion_times[k-1]
        completion_times[k] = enter_service_times[k] + service_times[k]

    system_size = empty(n_process)
    queue_size = zeros(n_process)
    for k in xrange(n_process):
        system_size[k] = (completion_times[:k][completion_times[:k] > arrival_times[k]]).size
        queue_size[k] = (enter_service_times[:k][enter_service_times[:k] >= arrival_times[k]]).size  

    def queue_size_by_time(time):
        return enter_service_times[(enter_service_times >= time) & (arrival_times < time)].size
   
    return { 
        'system_size' : system_size, 
        'queue_size' : queue_size,
        'queue_size_by_time': queue_size_by_time,
        'turnaround_time' : completion_times[-1],
        'wait_times' : enter_service_times - arrival_times,
        'enter_service_times': enter_service_times,
        'completion_times': completion_times

    }
