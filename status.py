#!/usr/bin/env python2
from __future__ import division

from math import sqrt
from sys import argv, exit
import subprocess
import datetime as dt
import re

# local imports
from my_pressure import pressure

def my_mean(*args):
    return sum(args)/len(args)

def my_means_std(*args):
    N = len(args)
    mean_value = my_mean(args)
    sum_squares = sum([ (x - mean_value)**2.0 for x in args ])
    return sqrt(sum_squares / (N*(N-1.0)))

if len(argv) <= 1:
    print("Provide std.out files as an argument.")
    exit(1)

status_regexp_time = " ([0-9]+:[0-9]+), ETA"
status_regexp_h = " ([0-9]+)hr"
status_regexp_m = " ([0-9]+)min"
status_regexp_s = " ([0-9]+)s,"
status_regexp_events = "Events ([0-9]+)k, t ([0-9\.]+), "

statuses = []
n_atoms = None

for file_name in argv[1:]:
    if n_atoms is None:
        with open(file_name, "r") as input_f:
            for line in input_f:
                n_atoms = re.search("Particle Count ([0-9]+)$", line)
                if n_atoms:
                    n_atoms = int(n_atoms.group(1))
                    break

    pid = int(re.search("std\.out\.([0-9]+).[0-9]+", file_name).group(1))
    status_line, _ = subprocess.Popen(["tail","-n 1 " + file_name],
            stdout=subprocess.PIPE).communicate()

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

pressure_mean = my_mean([s[-1] for s in statuses])
pressure_std = my_means_std([s[-1] for s in statuses])
print("\n\tAverage pressure: {:.10f} +- {:.10f} ({:.2e}).".format(
    pressure_mean, pressure_std, pressure_std / pressure_mean))
