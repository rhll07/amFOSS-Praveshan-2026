# Task-06: Pirate King's Scheduler

A small CPU scheduling simulator written in Go. Processes are treated as pirate crews waiting for their turn on the CPU.

## What it does ?

The program takes:

```text
Process ID  Arrival Time  Burst Time
```

and runs three CPU scheduling algorithms:

- **FCFS (First Come, First Served)**
- **SJF (Shortest Job First, non-preemptive)**
- **Round Robin**

For each algorithm, it shows:

- Execution order using a Gantt chart
- Waiting time for each process
- Turnaround time for each process
- Average waiting time
- Average turnaround time

For Round Robin, it also asks for a time quantum. If I just press Enter,
the default quantum is `2`.

## How to run

Make sure Go is installed, then run:

```bash
go run .
```

Or build it first:

```bash
go build -o scheduler .
./scheduler
```

The program asks for processes one by one:

```text
> 1 0 5
> 2 1 3
> 3 2 8
> 4 3 6
>
```

Press Enter on an empty line when all processes have been entered.

If no processes are entered, the program uses a default set of processes.

## Example

For the input:

```text
1 0 5
2 1 3
3 2 8
4 3 6
```

and a Round Robin quantum of `2`, the program produces output similar to:

```text
--- SJF (Shortest Job First, non-preemptive) ---

Execution order (Gantt chart):
+------+------+------+------+
|  P1  |  P2  |  P4  |  P3  |
+------+------+------+------+
0      5      8      14     22

Results:
Crew     Turnaround      Waiting
P1       5               0
P2       7               4
P3       20              12
P4       11              5

Average Waiting Time:      5.25
Average Turnaround Time:   10.75
```

## How I implemented it

The program is kept fairly small.

- `main.go` handles the input and runs all three algorithms.
- Each scheduling algorithm creates a list of execution slots.
- A shared function uses those slots to print the Gantt chart and calculate
  the results.

The main formulas used are:

```text
Turnaround Time = Completion Time - Arrival Time
Waiting Time    = Turnaround Time - Burst Time
```

For Round Robin, I used a simple FIFO ready queue. Processes are added to the
queue when they arrive, and a process is moved to the back of the queue if it
still has remaining burst time.

The scheduler also handles cases where the CPU is idle because no process has
arrived yet.

## What I learned

This task helped me understand how CPU scheduling actually works instead of
just reading about the algorithms.

I learned the difference between non-preemptive scheduling and time-sliced
scheduling, how a ready queue works in Round Robin, and how waiting and
turnaround times are calculated.

I also got more comfortable with Go input handling, slices, maps, sorting and
building a small program from scratch.

## Resources

- GeeksforGeeks — CPU scheduling algorithms
- Operating System Concepts — scheduling and process management
- Go documentation — `bufio`, slices, maps and sorting
