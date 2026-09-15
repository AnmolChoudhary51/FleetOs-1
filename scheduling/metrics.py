def calculate_metrics(results):
    total_waiting_time = 0
    total_turnaround_time = 0

    for result in results:
        total_waiting_time += result["waiting_time"]
        total_turnaround_time += result["turnaround_time"]

    number_of_missions = len(results)

    average_waiting_time = total_waiting_time / number_of_missions
    average_turnaround_time = total_turnaround_time / number_of_missions

    return average_waiting_time, average_turnaround_time