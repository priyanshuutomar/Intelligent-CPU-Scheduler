# main.py
# (content abbreviated for space)
# main.py
import argparse
import json
import os
from core import generate_random_workload, Simulator, Process, Burst
from schedulers import FCFS, SJF, RR, PriorityScheduler
import matplotlib.pyplot as plt

def parse_args():
    p = argparse.ArgumentParser(description="CPU Scheduling Simulator")
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--n', type=int, default=8)
    p.add_argument('--scheduler', type=str, default='rr', choices=['fcfs','sjf','rr','priority'])
    p.add_argument('--quantum', type=float, default=2.0)
    p.add_argument('--plot', action='store_true')
    p.add_argument('--outfile', type=str, default=None)
    p.add_argument('--num_cores', type=int, default=1)
    p.add_argument('--from_json', type=str, default=None, help='load workload from json file')
    return p.parse_args()

def load_from_json(path: str):
    with open(path, 'r') as f:
        data = json.load(f)
    procs = []
    for p in data['processes']:
        bursts = []
        for b in p['bursts']:
            bursts.append(Burst(cpu=float(b.get('cpu',0.0)), io=float(b.get('io',0.0))))
        procs.append(Process(pid=p['pid'], arrival=float(p['arrival']), bursts=bursts, priority=int(p.get('priority',0))))
    return procs

def plot_gantt(sim: Simulator, title: str='Gantt Chart', filename: str=None):
    procs = list(sim.process_table.values())
    fig, ax = plt.subplots(figsize=(10, 0.6 + 0.4 * len(procs)))
    for i, p in enumerate(sorted(procs, key=lambda x: x.arrival)):
        start = p.start_time if p.start_time is not None else p.arrival
        end = p.completion_time if p.completion_time is not None else start + max(0.1, p.current_cpu())
        ax.barh(i, end - start, left=start, height=0.4)
        ax.text(start + 0.01, i - 0.05, p.pid)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title(title)
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
        print(f"Saved gantt to {filename}")
    else:
        plt.show()

def main():
    args = parse_args()
    if args.from_json:
        processes = load_from_json(args.from_json)
    else:
        processes = generate_random_workload(n=args.n, seed=args.seed)

    if args.scheduler == 'fcfs':
        sched = FCFS()
    elif args.scheduler == 'sjf':
        sched = SJF()
    elif args.scheduler == 'rr':
        sched = RR(quantum=args.quantum)
    else:
        sched = PriorityScheduler()

    sim = Simulator(num_cores=args.num_cores, seed=args.seed, verbose=False)
    for p in processes:
        sim.add_process(p)

    results = sim.run(sched)
    print("=== RESULTS ===")
    print(json.dumps(results, indent=2))
    if args.plot:
        out = None
        if args.outfile:
            base = args.outfile
            if not os.path.isdir(os.path.dirname(base)) and os.path.dirname(base) != '':
                os.makedirs(os.path.dirname(base), exist_ok=True)
            out = base + "_gantt.png"
        plot_gantt(sim, title=f"{args.scheduler.upper()} Gantt", filename=out)

if __name__ == '__main__':
    main()
