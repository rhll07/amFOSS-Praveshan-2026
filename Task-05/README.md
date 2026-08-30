# Task 05 - Grand Line Guardian

A terminal-based Linux process monitoring tool inspired by utilities such as `htop` and `btop++`.

Grand Line Guardian continuously displays the processes currently running on the system and refreshes the information every 0.5 seconds.

## Features

### Mandatory

- Process ID (PID)
- Process name
- CPU usage
- Memory usage
- Total active process count
- Terminal-based interface
- Real-time updates at a 0.5-second interval

### Optional features implemented

- Navigate through the process list using the keyboard
- Move one process at a time with `↑` / `↓`
- Move one process at a time with `j` / `k`
- Move one screen at a time with `Page Up` / `Page Down`
- Jump to the first process with `Home`
- Jump to the last process with `End`
- Quit with `q`

Process termination was not implemented because it is optional.

## Requirements

- Linux
- Python 3
- `psutil`
- A terminal environment with curses support

## Installation

```bash
pip install -r requirements.txt
```

Alternatively:

```bash
pip3 install psutil
```

## Running

```bash
python3 monitor.py
```

The monitor refreshes every 0.5 seconds. Press `q` to exit.

## Example

```text
GRAND LINE GUARDIAN   Active Processes: 380
PID        NAME                         CPU%   MEM%
1          systemd                       0.0     0.2
2          kthreadd                      0.0     0.0
3          pool_workqueue_release        0.0     0.0
4          kworker/R-rcu_gp              0.0     0.0
...
```

When there are more processes than fit on the terminal, the list can be navigated using the keyboard controls.

## Approach

The application is implemented in Python using:

- `psutil` for process and system information
- Python's `curses` module for the terminal interface

The monitoring loop:

1. Enumerates running processes.
2. Collects PID and process name.
3. Calculates CPU and memory usage.
4. Counts active PIDs.
5. Draws the current process list.
6. Reads keyboard input for navigation.
7. Waits 0.5 seconds.
8. Repeats.

This keeps the process information live while allowing the user to move through the list.

## Process Information with psutil

`psutil.process_iter()` is used to enumerate processes:

```python
psutil.process_iter(["pid", "name"])
```

For each process, `oneshot()` is used while collecting information. CPU usage is obtained with:

```python
process.cpu_percent(interval=None)
```

and memory usage with:

```python
process.memory_percent()
```

The CPU value is divided by the number of logical CPUs so the displayed value represents usage relative to the whole machine.

The first CPU measurement for a process can be `0.0` because CPU percentage is calculated from a comparison between measurements. Later refreshes provide meaningful values.

## Handling Processes That Disappear

The process list can change while it is being read. A process may terminate between enumeration and information retrieval, or access may be denied.

The application handles:

- `psutil.NoSuchProcess`
- `psutil.AccessDenied`
- `psutil.ZombieProcess`

Processes that cannot be read are skipped rather than crashing the monitor.

## Terminal Interface

Python's `curses` module is used to create the live terminal interface.

It provides:

- Screen clearing and redrawing
- Position-based text output
- Keyboard input
- Terminal dimension detection
- A viewport for the process list

Only processes that fit in the current terminal window are displayed at once.

## Scrolling

A scroll offset is maintained when the process list is larger than the terminal.

| Key | Action |
|---|---|
| `↑` / `j` | Move up one process |
| `↓` / `k` | Move down one process |
| `Page Up` | Move up one screen |
| `Page Down` | Move down one screen |
| `Home` | Jump to the beginning |
| `End` | Jump to the end |
| `q` | Quit |

The process information continues to refresh while navigating.

## Linux `/proc` and the Kernel Interface

Linux exposes live operating-system information through the virtual `/proc` filesystem.

Each process normally has a directory such as:

```text
/proc/<PID>/
```

which contains kernel-provided information about that process. Examples include:

```text
/proc/<PID>/stat
/proc/<PID>/status
/proc/<PID>/cmdline
```

System-wide CPU and memory information is also exposed through `/proc`.

`psutil` provides a higher-level Python interface over these operating-system facilities, so this project does not need to manually parse `/proc`.

Understanding the relationship between kernel state, `/proc`, and process-monitoring tools was an important part of the task.

## Refresh Strategy

The refresh interval is:

```python
REFRESH = 0.5
```

The application therefore redraws approximately twice per second, satisfying the requirement for real-time updates or an update interval below one second.

## Resources Used

- psutil documentation: https://psutil.readthedocs.io/
- Python curses documentation: https://docs.python.org/3/library/curses.html
- Linux `/proc` documentation: `man 5 proc`

## New Concepts Learned

- Process enumeration and monitoring with `psutil`
- PID and process lifecycle concepts
- CPU and memory usage measurement
- The Linux `/proc` virtual filesystem
- The relationship between kernel process state and `/proc`
- Handling `NoSuchProcess`, `AccessDenied`, and `ZombieProcess`
- Using `curses` to build terminal user interfaces
- Reading keyboard input in a live terminal application
- Implementing scrolling over a continuously refreshed process list
- Periodic refresh loops for real-time monitoring

## Limitations

- Process termination is not implemented because it is optional.
- A process that disappears or cannot be accessed during collection is skipped.
- The application is intentionally lightweight rather than a full replacement for `htop` or `btop++`.