#!/usr/bin/env python3
import curses
import time
import psutil

REFRESH = 0.5

def get_processes():
    processes = []

    for p in psutil.process_iter(["pid", "name"]):
        try:
            with p.oneshot():
                cpu = p.cpu_percent(interval=None) / (psutil.cpu_count() or 1)
                mem = p.memory_percent()
                processes.append((
                    p.info["pid"],
                    p.info["name"] or "?",
                    cpu,
                    mem
                ))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    processes.sort(key=lambda x: x[0])
    return processes

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.timeout(100)

    scroll = 0

    while True:
        processes = get_processes()
        active = len(psutil.pids())

        height, width = stdscr.getmaxyx()
        visible = max(1, height - 2)
        maximum = max(0, len(processes) - visible)

        scroll = max(0, min(scroll, maximum))

        stdscr.erase()

        stdscr.addnstr(
            0, 0,
            f"GRAND LINE GUARDIAN   Active Processes: {active}",
            max(0, width - 1)
        )

        stdscr.addnstr(
            1, 0,
            f"{'PID':<10}{'NAME':<25}{'CPU%':>6}{'MEM%':>7}",
            max(0, width - 1)
        )

        for row, (pid, name, cpu, mem) in enumerate(
            processes[scroll:scroll + visible], 2
        ):
            line = f"{pid:<10}{name[:24]:<25}{cpu:6.1f}{mem:7.1f}"
            stdscr.addnstr(row, 0, line, max(0, width - 1))

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord("q") or key == ord("Q"):
            break

        elif key in (curses.KEY_DOWN, ord("j")):
            scroll = min(scroll + 1, maximum)
            curses.flushinp()

        elif key in (curses.KEY_UP, ord("k")):
            scroll = max(scroll - 1, 0)
            curses.flushinp()

        elif key == curses.KEY_NPAGE:
            scroll = min(scroll + visible, maximum)
            curses.flushinp()

        elif key == curses.KEY_PPAGE:
            scroll = max(scroll - visible, 0)
            curses.flushinp()

        elif key == curses.KEY_HOME:
            scroll = 0
            curses.flushinp()

        elif key == curses.KEY_END:
            scroll = maximum
            curses.flushinp()

        time.sleep(REFRESH)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass