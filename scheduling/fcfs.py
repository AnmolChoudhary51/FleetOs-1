def fcfs(missions):
    current_time = 0
    results = []

    for mission in missions:
        start_time = current_time
        completion_time = start_time + mission["burst_time"]

        waiting_time = start_time - mission["arrival_time"]
        turnaround_time = completion_time - mission["arrival_time"]

        results.append({
            "id": mission["id"],
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time
        })

        current_time = completion_time

    return results