from collections import defaultdict

def compute_metrics(events):
    events = sorted(events, key=lambda e: (e.worker_id, e.timestamp))

    worker = defaultdict(lambda: {"active":0,"idle":0,"units":0})
    station = defaultdict(lambda: {"occupancy":0,"units":0})

    for i in range(len(events)-1):
        curr, nxt = events[i], events[i+1]
        if curr.worker_id != nxt.worker_id:
            continue

        duration = (nxt.timestamp - curr.timestamp).total_seconds()

        if curr.event_type == "working":
            worker[curr.worker_id]["active"] += duration
            station[curr.workstation_id]["occupancy"] += duration
        elif curr.event_type == "idle":
            worker[curr.worker_id]["idle"] += duration

        if curr.event_type == "product_count":
            worker[curr.worker_id]["units"] += curr.count
            station[curr.workstation_id]["units"] += curr.count

    workers = []
    for wid, m in worker.items():
        total = m["active"] + m["idle"]
        util = (m["active"]/total*100) if total else 0
        uph = (m["units"]/(m["active"]/3600)) if m["active"] else 0
        workers.append({
            "worker_id": wid,
            "active_time": m["active"],
            "idle_time": m["idle"],
            "utilization_percent": util,
            "units": m["units"],
            "units_per_hour": uph
        })

    stations = []
    for sid, m in station.items():
        throughput = (m["units"]/(m["occupancy"]/3600)) if m["occupancy"] else 0
        stations.append({
            "station_id": sid,
            "occupancy_time": m["occupancy"],
            "units": m["units"],
            "throughput_rate": throughput
        })

    total_units = sum(w["units"] for w in workers)
    total_active = sum(w["active_time"] for w in workers)
    avg_util = sum(w["utilization_percent"] for w in workers)/len(workers) if workers else 0
    production_rate = total_units/(total_active/3600) if total_active else 0

    factory = {
        "total_units": total_units,
        "total_productive_time": total_active,
        "avg_utilization": avg_util,
        "production_rate": production_rate
    }

    return {"workers": workers, "workstations": stations, "factory": factory}