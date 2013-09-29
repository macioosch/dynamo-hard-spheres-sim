#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function

from datetime import datetime
from math import ceil, pi
from os import system
from random import random
from sys import argv
import calendar

# local imports
from my_helper_functions_bare import *

density = float(argv[1])
packing = density * pi/6

# Proper simulation:
min_n_atoms = 5e5
collisions_per_atom = 2e2
n_periods = 25

## Test:
#min_n_atoms = 5e3
#collisions_per_atom = 2e3
#n_periods = 20

run = 0

n_cells = int(ceil( (min_n_atoms/4)**(1/3) ))
n_atoms = 4*n_cells**3
total_collisions = int(collisions_per_atom * n_atoms)
collision_checkpoints = [ int(round(i)) for i in my_linspace(0,
        total_collisions, n_periods+1) ]

utcnow = datetime.utcnow()
microtimestamp = int(calendar.timegm(utcnow.utctimetuple())*1e6 + utcnow.microsecond)
random_flavour = int(999999 * random())
base_name = "{}_{:0.12f}_{}{:06d}".format(n_atoms, packing, microtimestamp,
        random_flavour) + "_{0:02d}_"

system(("[ -f configs/" + base_name + "0.xml ] || dynamod -m 0 "
        "-C {1} -d {2} --i1 0 -r 1 -o configs/" + base_name + "0.xml").format(
                run, n_cells, density))

for c0, c1 in zip(collision_checkpoints[:-1], collision_checkpoints[1:]):
    system(("[ -f results/" + base_name + "{1}_{3}.xml.bz2 ] || "
    "dynarun -L MSD configs/" + base_name + "{1}.xml -c {2} -o configs/"
    + base_name + "{3}.xml --out-data-file results/" + base_name
    + "{1}_{3}.xml.bz2").format(run, c0, c1-c0, c1))
    system(("rm -v configs/" + base_name + "{1}.xml").format(run, c0))
