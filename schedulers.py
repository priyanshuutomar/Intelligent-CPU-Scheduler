# schedulers.py
# (content abbreviated for space)
# schedulers.py
from typing import Optional, Tuple
from core import Process, Simulator

class SchedulerBase:
    def on_sim_start(self, sim: Simulator): pass
    def on_sim_end(self, sim: Simulator): pass
    def on_new_process(self, proc: Process, time: float): pass
    def on_io_complete(self, proc: Process, time: float): pass
    def on_preempt(self, proc: Process, core_id: int, time: float): pass
    def on_complete(self, proc: Process, core_id: int, time: float): pass
    def on_block(self, proc: Process, core_id: int, time: float, io_time: float): pass
    def on_return_from_io(self, proc: Process, core_id: int, time: float): pass
    def select_next(self, sim: Simulator, core_id: int, time: float) -> Optional[Tuple[Process, float]]:
        raise NotImplementedError

# FCFS (non-preemptive) - run full burst
class FCFS(SchedulerBase):
    def select_next(self, sim: Simulator, core_id: int, time: float):
        if sim.ready:
            proc = sim.ready[0]
            return (proc, proc.current_cpu())
        return None

# SJF (non-preemptive) - choose shortest remaining CPU
class SJF(SchedulerBase):
    def select_next(self, sim: Simulator, core_id: int, time: float):
        if not sim.ready:
            return None
        proc = min(list(sim.ready), key=lambda p: p.current_cpu())
        return (proc, proc.current_cpu())

# Round Robin
class RR(SchedulerBase):
    def __init__(self, quantum: float = 2.0):
        self.quantum = quantum

    def select_next(self, sim: Simulator, core_id: int, time: float):
        if not sim.ready:
            return None
        proc = sim.ready[0]
        return (proc, self.quantum)

# Priority Scheduling (higher priority -> smaller number means higher priority)
# Non-preemptive by default; can be easily extended to preemptive by checking running proc priority
class PriorityScheduler(SchedulerBase):
    def select_next(self, sim: Simulator, core_id: int, time: float):
        if not sim.ready:
            return None
        proc = min(list(sim.ready), key=lambda p: p.priority)
        return (proc, proc.current_cpu())
