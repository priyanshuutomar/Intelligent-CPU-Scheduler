
🖥️ Intelligent CPU Scheduler Simulator

This project simulates CPU scheduling algorithms using interactive user input and displays scheduling results such as completion time, waiting time, and turnaround time.

✔ Supported Scheduling Algorithms

FCFS (First Come First Serve)

Round Robin

Priority Scheduling

✔ Features

User-defined process input

Arrival Time

Burst Time

Priority (for Priority Scheduling)

Time Quantum (for Round Robin)

Displays:

Completion Time (CT)

Waiting Time (WT)

Turnaround Time (TAT)

Clean and easy-to-understand console output

Modular Python code with team-based structure

📦 Files in This Project
File Name	Description
main_scheduler.py	Main file that takes user input and runs selected scheduling algorithm
core_fcfs.py	Implementation of FCFS scheduling algorithm
core_priority.py	Implementation of Priority Scheduling algorithm
core_rr.py	Implementation of Round Robin scheduling algorithm
README.md	Project documentation
▶ How to Run

Open the project folder in VS Code or any Python IDE

Run the following command in terminal:

python main_scheduler.py


Enter inputs as prompted:

Enter your choice:
Enter number of processes:
Enter arrival time for P1:
Enter burst time for P1:
Enter priority for P1:

📊 Sample Output
ROUND ROBIN SCHEDULING
Process  AT  BT  CT  TAT  WT
P1       0   5   10  10   5
P2       1   3   7   6    3

🛠️ Technologies Used

Python 3.x

Visual Studio Code

Git & GitHub

👥 Team Members

Priyanshu Tomar (Roll No. 21) – Round Robin & Integration

Althamas Hussain (Roll No. 28) – Priority Scheduling

Kratika Tiwari (Roll No. 15) – FCFS Scheduling
