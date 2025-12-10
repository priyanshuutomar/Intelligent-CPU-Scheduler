# core.py
# (content abbreviated for space in this environment, but full content should be inserted here)
# For actual usage, paste full code you provided earlier.
# core.py
import heapq
import random
from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Tuple

@dataclass
class Burst:
    cpu: float
    io: float = 0.0

@dataclass
class Process:
    pid: str
    arrival: float
    bursts: List[Burst]
    priority: int = 0

    # runtime bookkeeping
    cur_burst_idx: int = 0
    remaining: float = 0.0
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    last_start_time: Optional[float] = None
    total_wait: float = 0.0
    first_response_recorded: bool = False
    response_time: Optional[float] = None

    def is_done(self) -> bool:
        return self.cur_burst_idx >= len(self.bursts)

    def current_cpu(self) -> float:
        if self.is_done():
            return 0.0
        if self.remaining > 0:
            return self.remaining
        return self.bursts[self.cur_burst_idx].cpu

    def consume_cpu(self, amount: float) -> float:
        if self.remaining <= 0:
            self.remaining = self.bursts[self.cur_burst_idx].cpu
        use = min(self.remaining, amount)
        self.remaining -= use
        if self.remaining <= 1e-9:
            self.cur_burst_idx += 1
            self.remaining = 0.0
        return use

    def next_io(self) -> float:
        # io corresponding to burst just finished
        idx = self.cur_burst_idx - 1
        if 0 <= idx < len(self.bursts):
            return self.bursts[idx].io
        return 0.0

@dataclass(order=True)
class Event:
    time: float
    order: int
    etype: str = field(compare=False)
    payload: Any = field(compare=False, default=None)

class Simulator:
    def __init__(self, num_cores: int = 1, seed: Optional[int] = None, verbose: bool = False):
        self.time = 0.0
        self.event_q: List[Event] = []
        self._ev_counter = 0
        self.ready: deque = deque()
        self.blocked: List[Tuple[float, Process]] = []
        self.running: List[Optional[Process]] = [None] * num_cores
        self.num_cores = num_cores
        self.process_table: Dict[str, Process] = {}
        self.verbose = verbose
        if seed is not None:
            random.seed(seed)

    def log_event(self, time: float, etype: str, payload: Any = None):
        ev = Event(time, self._ev_counter, etype, payload)
        self._ev_counter += 1
        heapq.heappush(self.event_q, ev)

    def add_process(self, p: Process):
        self.process_table[p.pid] = p
        self.log_event(p.arrival, 'ARRIVAL', p.pid)

    def run(self, scheduler, until: Optional[float] = None):
        scheduler.on_sim_start(self)
        while self.event_q:
            ev = heapq.heappop(self.event_q)
            self.time = ev.time
            if until is not None and self.time > until:
                break
            if self.verbose:
                print(f"[t={self.time:.3f}] Event: {ev.etype} -> {ev.payload}")
            if ev.etype == 'ARRIVAL':
                pid = ev.payload
                proc = self.process_table[pid]
                proc.last_start_time = None
                self.ready.append(proc)
                scheduler.on_new_process(proc, self.time)
            elif ev.etype == 'IO_COMPLETE':
                pid = ev.payload
                proc = self.process_table[pid]
                self.ready.append(proc)
                scheduler.on_io_complete(proc, self.time)
            elif ev.etype == 'CPU_QUANTUM_EXPIRE':
                core_id, pid = ev.payload
                running = self.running[core_id]
                if running and running.pid == pid:
                    scheduler.on_preempt(running, core_id, self.time)
                    # mark running slot free; scheduler will reassign
                    self.running[core_id] = None
            elif ev.etype == 'CPU_BURST_COMPLETE':
                core_id, pid = ev.payload
                running = self.running[core_id]
                if running and running.pid == pid:
                    io_t = running.next_io()
                    if running.is_done():
                        running.completion_time = self.time
                        scheduler.on_complete(running, core_id, self.time)
                    elif io_t > 0:
                        self.log_event(self.time + io_t, 'IO_COMPLETE', running.pid)
                        scheduler.on_block(running, core_id, self.time, io_t)
                    else:
                        self.ready.append(running)
                        scheduler.on_return_from_io(running, core_id, self.time)
                    self.running[core_id] = None
            # scheduling attempt for idle cores
            for core_id in range(self.num_cores):
                if self.running[core_id] is None:
                    choice = scheduler.select_next(self, core_id, self.time)
                    if choice:
                        proc, run_for = choice
                        self._dispatch(proc, core_id, run_for, scheduler)
        scheduler.on_sim_end(self)
        return self.collect_metrics()

    def _dispatch(self, proc: Process, core_id: int, run_for: float, scheduler):
        try:
            self.ready.remove(proc)
        except ValueError:
            pass
        if proc.start_time is None:
            proc.start_time = self.time
        if not proc.first_response_recorded:
            proc.response_time = self.time - proc.arrival
            proc.first_response_recorded = True
        proc.last_start_time = self.time
        self.running[core_id] = proc
        consumed = proc.consume_cpu(run_for)
        if proc.is_done() or proc.remaining == 0:
            self.log_event(self.time + consumed, 'CPU_BURST_COMPLETE', (core_id, proc.pid))
        else:
            self.log_event(self.time + consumed, 'CPU_QUANTUM_EXPIRE', (core_id, proc.pid))

    def collect_metrics(self):
        procs = list(self.process_table.values())
        completed = [p for p in procs if p.completion_time is not None]
        results = {}
        if completed:
            results['avg_turnaround'] = sum((p.completion_time - p.arrival) for p in completed) / len(completed)
            results['avg_waiting'] = sum(p.total_wait for p in completed) / len(completed)
            responses = [p.response_time for p in completed if p.response_time is not None]
            results['avg_response'] = sum(responses) / len(responses) if responses else None
            makespan = max(p.completion_time for p in completed)
            results['throughput'] = len(completed) / max(1.0, makespan)
        else:
            results['avg_turnaround'] = None
            results['avg_waiting'] = None
            results['avg_response'] = None
            results['throughput'] = 0
        results['per_process'] = {p.pid: {'arrival': p.arrival,
                                         'completion': p.completion_time,
                                         'turnaround': (p.completion_time - p.arrival) if p.completion_time else None,
                                         'waiting': p.total_wait,
                                         'response': p.response_time}
                                  for p in procs}
        return results

# Workload generator
def generate_random_workload(n: int = 8, arrival_lambda: float = 1.0, cpu_mean: float = 5.0,
                             io_prob: float = 0.3, io_mean: float = 2.0, seed: Optional[int] = None) -> List[Process]:
    if seed is not None:
        random.seed(seed)
    procs = []
    t = 0.0
    for i in range(1, n + 1):
        ia = random.expovariate(arrival_lambda)
        t += ia
        bursts = []
        num_bursts = random.choice([1, 1, 2, 2, 3])
        for b in range(num_bursts):
            cpu = max(0.1, random.expovariate(1.0 / cpu_mean))
            io = 0.0
            if b < num_bursts - 1 and random.random() < io_prob:
                io = max(0.1, random.expovariate(1.0 / io_mean))
            bursts.append(Burst(cpu=round(cpu, 3), io=round(io, 3)))
        pid = f'P{i}'
        prio = random.randint(0, 4)
        procs.append(Process(pid=pid, arrival=round(t, 3), bursts=bursts, priority=prio))
    return procs
