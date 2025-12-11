from core_fcfs import fcfs
from core_priority import priority_scheduling
from core_rr import round_robin

print("CPU SCHEDULING SIMULATOR")
print("1. FCFS")
print("2. Priority Scheduling")
print("3. Round Robin")

choice = int(input("Enter your choice: "))

n = int(input("Enter number of processes: "))
processes = []

for i in range(n):
    print(f"\nProcess P{i+1}:")
    at = int(input(f"Enter arrival time for P{i+1}: "))
    bt = int(input(f"Enter burst time for P{i+1}: "))

    if choice == 2:
        pr = int(input(f"Enter priority for P{i+1}: "))
        processes.append([f"P{i+1}", at, bt, pr])
    else:
        processes.append([f"P{i+1}", at, bt])

if choice == 3:
    tq = int(input("Enter Time Quantum: "))

print("\n--- OUTPUT ---")

if choice == 1:
    fcfs(processes)

elif choice == 2:
    priority_scheduling(processes)

elif choice == 3:
    round_robin(processes, tq)

else:
    print("Invalid choice!")