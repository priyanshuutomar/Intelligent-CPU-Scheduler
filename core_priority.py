def priority_scheduling(processes):
    processes.sort(key=lambda x: (x[1], x[3]))

    time = 0
    print("\nPRIORITY SCHEDULING:")
    print("Process\tAT\tBT\tPR\tCT\tTAT\tWT")

    for p in processes:
        name, at, bt, pr = p

        if time < at:
            time = at

        ct = time + bt
        tat = ct - at
        wt = tat - bt

        time = ct

        print(f"{name}\t{at}\t{bt}\t{pr}\t{ct}\t{tat}\t{wt}")