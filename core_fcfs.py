def fcfs(processes):
    processes.sort(key=lambda x: x[1])

    time = 0
    print("\nFCFS SCHEDULING:")
    print("Process\tAT\tBT\tCT\tTAT\tWT")

    for p in processes:
        name, at, bt = p

        if time < at:
            time = at

        ct = time + bt
        tat = ct - at
        wt = tat - bt

        time = ct

        print(f"{name}\t{at}\t{bt}\t{ct}\t{tat}\t{wt}")