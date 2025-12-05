
# Intelligent CPU Scheduler Simulator

This project simulates CPU scheduling algorithms with real-time Gantt chart visualization.

## ✔ Supported Scheduling Algorithms
- FCFS (First Come First Serve)
- SJF (Shortest Job First)
- Round Robin
- Priority Scheduling

## ✔ Features
- Input processes (arrival time, burst time, priority)
- Generates Gantt charts using matplotlib
- Prints metrics:
  - Waiting Time
  - Turnaround Time
  - Completion Time
- Works with CLI arguments

## 📦 Files in This Project
| File | Description |
|------|-------------|
| **core.py** | Core engine + Process class + helper functions |
| **schedulers.py** | All scheduling algorithm implementations |
| **main.py** | User interface, charts, command-line runner |
| **requirements.txt** | Libraries required (matplotlib) |

---

## ▶ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
