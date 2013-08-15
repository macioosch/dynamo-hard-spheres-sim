#!/usr/bin/env python3
from glob import glob
from subprocess import getoutput
import datetime as dt
import numpy as np
import re

def pressure(n_atoms, n_coll, delta_t):
    # only when m = \sigma = \beta = \gamma(n_atoms) = 1.0
    # const_var is a static variable
    if "const_var" not in pressure.__dict__:
        pressure.const_var = np.sqrt(np.pi) / (3*n_atoms)
    return 1.0 + pressure.const_var * n_coll / delta_t

status_regexp_time = " ([0-9]+:[0-9]+), ETA"
status_regexp_h = " ([0-9]+)hr"
status_regexp_m = " ([0-9]+)min"
status_regexp_s = " ([0-9]+)s,"
status_regexp_events = "Events ([0-9]+)k, t ([0-9\.]+), "

statuses = []
n_atoms = None

for file_name in glob("stdouterr/std.out.*"):
    if n_atoms is None:
        with open(file_name, "r") as input_f:
            for line in input_f:
                n_atoms = re.search("Particle Count ([0-9]+)$", line)
                if n_atoms:
                    n_atoms = int(n_atoms.group(1))
                    break

    pid = int(re.match("stdouterr/std\.out\.([0-9]+)", file_name).group(1))
    status_line = getoutput("tail -n 1 " + file_name)

    log_time = re.search(status_regexp_time, status_line).group(1)
    log_date = dt.datetime.strptime(log_time, "%H:%M")
    today = dt.date.today()
    log_date = log_date.replace(year=today.year, month=today.month, day=today.day)
    
    h = re.search(status_regexp_h, status_line)
    if h: h = int(h.group(1))
    else: h = 0
    m = re.search(status_regexp_m, status_line)
    if m: m = int(m.group(1))
    else: m = 0
    s = re.search(status_regexp_s, status_line)
    if s: s = int(s.group(1))
    else: s = 0
    estimate = dt.timedelta(hours=h, minutes=m, seconds=s)

    events, sim_time = re.search(status_regexp_events, status_line).groups()
    events = 1000 * int(events)
    sim_time = float(sim_time)

    statuses.append([pid, log_date + estimate, pressure(n_atoms, events, sim_time)])

for pid_status in sorted(statuses, key=lambda x: x[1]):
    print("Process {} will end around {}. Pressure: {}.".format(*pid_status[:3]))

pressure_mean = np.mean([s[-1] for s in statuses])
pressure_std = np.std([s[-1] for s in statuses])
print("\n\tAverage pressure: {:.10f} +- {:.10f} ({:.2e}).".format(
    pressure_mean, pressure_std, pressure_std / pressure_mean))

