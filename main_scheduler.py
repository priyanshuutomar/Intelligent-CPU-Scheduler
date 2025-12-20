from core_fcfs import fcfs
from core_priority import priority_scheduling
from core_rr import round_robin

def run_all(processes_basic, processes_priority, tq):

    print("===== FCFS =====")
    fcfs(processes_basic)

    print("\n===== PRIORITY =====")
    priority_scheduling(processes_priority)

    print("\n===== ROUND ROBIN =====")
    round_robin(processes_basic, tq)
