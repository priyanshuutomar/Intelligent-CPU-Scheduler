def round_robin(processes, tq):
    n = len(processes)
    rem_bt = [p[2] for p in processes]
    time = 0
    completed = 0

    print("\nROUND ROBIN SCHEDULING:")
    print("Process\tAT\tBT\tCT\tTAT\tWT")

    ct = [0]*n

    while completed < n:
        done = True

        for i in range(n):
            name, at, bt = processes[i]

            if rem_bt[i] > 0 and at <= time:
                done = False

                if rem_bt[i] > tq:
                    time += tq
                    rem_bt[i] -= tq
                else:
                    time += rem_bt[i]
                    rem_bt[i] = 0
                    ct[i] = time
                    completed += 1

        if done:
            time += 1

    for i in range(n):
        name, at, bt = processes[i]
        tat = ct[i] - at
        wt = tat - bt
        print(f"{name}\t{at}\t{bt}\t{ct[i]}\t{tat}\t{wt}")