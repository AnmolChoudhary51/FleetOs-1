from fcfs import fcfs
from metrics import calculate_metrics

missions = [
    {"id": "M1", "arrival_time": 0, "burst_time": 5},
    {"id": "M2", "arrival_time": 1, "burst_time": 3},
    {"id": "M3", "arrival_time": 2, "burst_time": 8},
    {"id": "M4", "arrival_time": 3, "burst_time": 2}
]

results = fcfs(missions)

for result in results:
    print(result)

average_wt, average_tat = calculate_metrics(results)

print("Average Waiting Time:", average_wt)
print("Average Turnaround Time:", average_tat)