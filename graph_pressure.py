#!/usr/bin/env python2
"""
    For this to work, logging must be config-wise, not pid-wise!
"""
from glob import glob
from pprint import pprint
import numpy as np
import re

# local imports
from my_helper_functions import my_pressure

status_regexp_events = "Events ([0-9]+)k, t ([0-9\.]+), "

partial_results = []
n_atoms = None

for file_name in glob("stdouterr/std.out.*"):
    with open(file_name, "r") as input_f:
        # add a new array for results from another process
        partial_results.append([])
        collision_offset = 0
        time_offset = 0.0

        for line in input_f:
            if n_atoms is None:
                n_atoms = re.search("Particle Count ([0-9]+)$", line)
                if n_atoms:
                    n_atoms = int(n_atoms.group(1))
                    break

            line_results = re.search(status_regexp_events, line)

            if line_results:
                events, sim_time = line_results.groups()

                events = 1000 * int(events) + collision_offset
                sim_time = float(sim_time) + time_offset

                if len(partial_results[-1]) >= 1 \
                        and events < partial_results[-1][-1][1]:
                    collision_offset = partial_results[-1][-1][1]
                    time_offset = partial_results[-1][-1][2]

                partial_results[-1].append([events, sim_time,
                    pressure(n_atoms, events, sim_time)])

pprint(partial_results)
