# Task 05 — Grand Line Guardian

A tiny terminal process monitor, htop-style but as simple as possible. It shows
a live table of every running process on the machine and keeps refreshing it
about twice a second while you watch.

Every row is a "ship" sailing the Grand Line:

```
GRAND LINE GUARDIAN   Active Processes: 358
PID        NAME                         CPU%   MEM%
1          systemd                        0.0    0.2
2          kthreadd                       0.0    0.0
842        gnome-shell                    2.4    3.2
1234       firefox                        8.7    5.1
...
```

## What it shows

For each process (well, for each one we can read, more on that below):

- PID — the numeric process id
- Name — the process name
- CPU % — how much of one core the process is using
- MEM % — what share of total RAM it's consuming

On top there's the total active process count, which updates every frame.

## Installing

The only dependency is `psutil`:

```bash
pip install -r requirements.txt
```

(Or `pip3 install psutil` if you're not using a virtualenv.)

## Running

```bash
python3 monitor.py
```

Press `Ctrl+C` to stop it.

## How it works

### Getting the process info

`psutil` does the heavy lifting. For each process it reports the PID, name,
CPU% and memory%. I call `cpu_percent()` and `memory_percent()` inside
`p.oneshot()`, which caches all the process info from one `/proc` read instead
of reading it several times separately — a small performance win.

One gotcha: `psutil`'s `cpu_percent()` returns 0 the first time you call it for
a process and the real value on later calls, because it compares CPU time
between two snapshots. So the table shows 0.0 on the very first frame and real
numbers from then on. That's normal and how tools like htop behave.

The program prints text to the terminal using `curses`. `curses` gives us
"draw at this row and column" control, so we can overwrite the same lines each
tick instead of printing an endless scroll.

### The refresh loop

The whole thing is one `while True` loop:

1. Erase the screen.
2. Loop over all processes and collect their info (skipping any that fail).
3. Print the table.
4. `time.sleep(0.5)` and repeat.

So it redraws roughly twice a second. Every redraw is a fresh read, so the
numbers and the process list stay current.

## How it survives dying / unreadable processes

The Linux process list changes constantly — processes exit while we're reading
them, and some (like root-owned system daemons) refuse to give us info, plus a
few are zombie processes that have exited but are waiting for their parent.

If we didn't handle these, the program would throw and crash the moment any
process disappeared. So the per-process read is wrapped in a try/except that
catches exactly the three relevant errors from `psutil`:

- `NoSuchProcess` — the process ended between the list and our read
- `AccessDenied` — the OS won't let us read it
- `ZombieProcess` — the process is already dead but not yet reaped

Any process that errors out is simply skipped and we move on to the next one.
The monitor keeps going and never crashes. The terminal resize is handled by
curses, and I use `getmaxyx()` to keep lines from spilling past the screen edge.

## The Linux `/proc` concept

The reason `psutil` can do this at all is the Linux **virtual filesystem** at
`/proc`. On Linux, there's no "API call" to list processes — instead the kernel
exposes almost everything as files and directories under `/proc`.

Each running process has a directory `/proc/<pid>` (e.g. `/proc/1234`) filled
with files describing it: `name`, `cmdline`, `stat`, `status`, `meminfo` and so
on. `psutil` reads these files (and `/proc/stat` for global CPU numbers) and
gives us a clean Python API on top.

`process_iter`/`cpu_percent` are just a friendly wrapper around that same
kernel interface. So "process management and the Linux kernel interface" here
means: the kernel stores live process state in `/proc`, and we read it through
`psutil`.

You *could* read `/proc` directly with plain Python, but `psutil` already
handles all the parsing and edge cases (including the NoSuchProcess /
AccessDenied cases above), so for this task using it is the clean choice.

## Files

```
Task-05/
├── monitor.py       # the whole program
├── requirements.txt # psutil
└── README.md
```

## Resources

- [psutil docs](https://psutil.readthedocs.io/) — process_iter, cpu_percent,
  memory_percent, oneshot
- [Python curses docs](https://docs.python.org/3/howto/curses.html)
- `man 5 proc` — describes what the `/proc` filesystem contains

## Things I learned

- The first `cpu_percent()` call always returns 0 until there's a second call
  to compare against.
- `p.oneshot()` batches all the `/proc` reads for a single process into one
  pass, which is notably faster.
- Curses lets you place text at exact coordinates, which is how in-place
  terminals GUIs (htop, btop, vim status lines) work under the hood.
- How insanely volatile the process list is — you really do get
  `NoSuchProcess`/`AccessDenied` constantly on a busy system, so every tool
  that lists processes has to tolerate those errors.
- `/proc` isn't real disk storage; it's a view into kernel state, which is why
  it works for live monitoring.
