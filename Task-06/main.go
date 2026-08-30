package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Process struct {
	ID    int
	Arr   int
	Burst int
}

type Slot struct {
	ID   int
	From int
	To   int
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	processes := inputProcesses(reader)

	fmt.Println("\nPirate King's Scheduler")
	fmt.Println("=======================")
	fmt.Println("\nJobs waiting to sail across the Grand Line:")
	fmt.Printf("%-8s %-15s %-15s\n", "Crew", "Arrival Time", "Burst Time")
	for _, p := range processes {
		fmt.Printf("P%-7d %-15d %-15d\n", p.ID, p.Arr, p.Burst)
	}

	quantum := 2
	fmt.Print("\nTime quantum for Round Robin (just Enter for 2): ")
	line, _ := reader.ReadString('\n')
	if line = strings.TrimSpace(line); line != "" {
		quantum, _ = strconv.Atoi(line)
		if quantum < 1 {
			quantum = 1
		}
	}

	fmt.Println("\n--- FCFS (First Come, First Served) ---")
	fcfs(processes)

	fmt.Println("\n--- SJF (Shortest Job First, non-preemptive) ---")
	sjf(processes)

	fmt.Printf("\n--- Round Robin (quantum = %d) ---\n", quantum)
	roundRobin(processes, quantum)
}

func inputProcesses(reader *bufio.Reader) []Process {
	var processes []Process
	fmt.Println("Pirate King's Scheduler")
	fmt.Println("=======================")
	fmt.Println("Enter each crew as: processID arrivalTime burstTime")
	fmt.Println("Press Enter on an empty line when done.")

	for {
		fmt.Print("> ")
		line, _ := reader.ReadString('\n')
		if strings.TrimSpace(line) == "" {
			break
		}
		parts := strings.Fields(line)
		if len(parts) != 3 {
			fmt.Println("  Expected 3 numbers: ID arrival burst. Try again.")
			continue
		}
		id, err1 := strconv.Atoi(parts[0])
		arr, err2 := strconv.Atoi(parts[1])
		burst, err3 := strconv.Atoi(parts[2])
		if err1 != nil || err2 != nil || err3 != nil || burst < 1 {
			fmt.Println("  Invalid numbers. ID and times must be integers, burst >= 1.")
			continue
		}
		processes = append(processes, Process{ID: id, Arr: arr, Burst: burst})
	}

	if len(processes) == 0 {
		fmt.Println("No crews entered, using a default set instead.")
		processes = []Process{
			{ID: 1, Arr: 0, Burst: 5},
			{ID: 2, Arr: 1, Burst: 3},
			{ID: 3, Arr: 2, Burst: 8},
			{ID: 4, Arr: 3, Burst: 6},
		}
	}
	return processes
}

func run(processes []Process, slots []Slot) {
	if len(slots) == 0 {
		fmt.Println("\nNo processes to schedule.")
		return
	}

	// completion time for each process
	completion := map[int]int{}
	for _, s := range slots {
		completion[s.ID] = s.To
	}

	fmt.Println("\nExecution order (Gantt chart):")
	for range slots {
		fmt.Print("+------")
	}
	fmt.Println("+")

	for _, s := range slots {
		fmt.Printf("|  P%-3d", s.ID)
	}
	fmt.Println("|")

	for range slots {
		fmt.Print("+------")
	}
	fmt.Println("+")

	for _, s := range slots {
		fmt.Printf("%-7d", s.From)
	}
	fmt.Printf("%d\n", slots[len(slots)-1].To)

	fmt.Println("\nResults:")
	fmt.Printf("%-8s %-15s %-15s\n", "Crew", "Turnaround", "Waiting")
	var totalWt, totalTat int
	for _, p := range processes {
		tat := completion[p.ID] - p.Arr
		wt := tat - p.Burst
		totalTat += tat
		totalWt += wt
		fmt.Printf("P%-7d %-15d %-15d\n", p.ID, tat, wt)
	}
	n := len(processes)
	fmt.Printf("\nAverage Waiting Time:      %.2f\n", float64(totalWt)/float64(n))
	fmt.Printf("Average Turnaround Time:   %.2f\n", float64(totalTat)/float64(n))
}

func fcfs(processes []Process) {
	byArrival(processes)

	var slots []Slot
	current := 0
	for _, p := range processes {
		if current < p.Arr {
			current = p.Arr
		}
		slots = append(slots, Slot{ID: p.ID, From: current, To: current + p.Burst})
		current += p.Burst
	}
	run(processes, slots)
}

func sjf(processes []Process) {
	remaining := make([]Process, len(processes))
	copy(remaining, processes)

	var slots []Slot
	current := 0
	for len(remaining) > 0 {
		// pick the shortest burst among processes that have arrived
		best := -1
		for i, p := range remaining {
			if p.Arr <= current && (best == -1 || p.Burst < remaining[best].Burst) {
				best = i
			}
		}
		if best == -1 {
			// idle until the next process arrives
			next := remaining[0].Arr
			for _, p := range remaining {
				if p.Arr < next {
					next = p.Arr
				}
			}
			current = next
			continue
		}
		pick := remaining[best]
		slots = append(slots, Slot{ID: pick.ID, From: current, To: current + pick.Burst})
		current += pick.Burst
		remaining = append(remaining[:best], remaining[best+1:]...)
	}
	run(processes, slots)
}

func roundRobin(processes []Process, quantum int) {
	ordered := make([]Process, len(processes))
	copy(ordered, processes)
	byArrival(ordered)

	remaining := map[int]int{}
	for _, p := range processes {
		remaining[p.ID] = p.Burst
	}

	var slots []Slot
	queue := []int{}
	inQueue := map[int]bool{}
	current := 0

	addArrivals := func() {
		for _, p := range ordered {
			if p.Arr <= current && !inQueue[p.ID] {
				queue = append(queue, p.ID)
				inQueue[p.ID] = true
			}
		}
	}

	// keep going until every process is both added and finished
	for len(inQueue) < len(processes) || len(queue) > 0 {
		addArrivals()
		if len(queue) == 0 {
			// idle until the next process arrives
			for _, p := range ordered {
				if !inQueue[p.ID] {
					current = p.Arr
					break
				}
			}
			continue
		}
		id := queue[0]
		queue = queue[1:]
		runFor := quantum
		if remaining[id] < runFor {
			runFor = remaining[id]
		}
		slots = append(slots, Slot{ID: id, From: current, To: current + runFor})
		current += runFor
		remaining[id] -= runFor
		// processes that arrived during this slice join the queue first
		addArrivals()
		if remaining[id] > 0 {
			queue = append(queue, id)
		}
	}
	run(processes, slots)
}

func byArrival(processes []Process) {
	sort.Slice(processes, func(i, j int) bool {
		if processes[i].Arr == processes[j].Arr {
			return processes[i].ID < processes[j].ID
		}
		return processes[i].Arr < processes[j].Arr
	})
}
