#!/usr/bin/env python3
import curses
import psutil
import time

REFRESH = 0.5


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)

    while True:
        stdscr.erase()

        procs = []
        for p in psutil.process_iter(["pid", "name"]):
            try:
                with p.oneshot():
                    cpu = p.cpu_percent(interval=None) / psutil.cpu_count()
                    mem = p.memory_percent()
                    procs.append((p.info["pid"], p.info["name"] or "?", cpu, mem))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        h, w = stdscr.getmaxyx()
        header = f"GRAND LINE GUARDIAN   Active Processes: {len(procs)}"
        stdscr.addstr(0, 0, header[:w])
        stdscr.addstr(1, 0, ("PID" + " " * 9 + "NAME" + " " * 24 + "CPU%   MEM%")[:w])

        row = 2
        for pid, name, cpu, mem in procs:
            if row >= h:
                break
            line = f"{pid:<10}{name[:24]:<25}{cpu:6.1f}{mem:6.1f}"
            stdscr.addstr(row, 0, line[:w])
            row += 1

        stdscr.refresh()
        time.sleep(REFRESH)


if __name__ == "__main__":
    curses.wrapper(main)
