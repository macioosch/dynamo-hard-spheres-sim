#!/usr/bin/env python2
from __future__ import division

import argparse
import calendar
import re
from datetime import datetime
from functools import partial
from glob import glob
from math import ceil, pi
from multiprocessing import Pool, cpu_count
from os import remove, rename, system, getpid
from pprint import pprint
from random import randint

def safe_runner(command, jid=None):
    try:
        system(command + " 1>>log/std.out.{0}.{1} 2>>log/std.err.{0}.{1}"
                .format(jid, getpid()))
        print("Command '{}' done by process {}.".format(command, getpid()))
    except:
        print("Oops! Command '{}' didn't work.".format(command))

def move_peeks(base_name, collisions, period):
    for snapshot in glob("Snapshot.output.*.xml.bz2"):
        number = 1 + int(re.match("Snapshot\.output\.([0-9]+)e?\.xml\.bz2",
                snapshot).group(1))
        new_name = "peeks/" + base_name.format(0) + "{}_{}.xml.bz2".format(
                collisions, collisions + number*period)
        rename(snapshot, new_name)
    for unneded_config in glob("Snapshot.*.xml.bz2"):
        remove(unneded_config)

"""
    Parsing command line agruments.
"""

parser = argparse.ArgumentParser(
        description="Run multiprocess DynamO simulations with given "
        "parameters.")
parser.add_argument("-c", "--collisions", type=int, default=1000000,
        help="number of simulated collisions after equlibrating (default: "
        "1000000)")
parser.add_argument("-e", "--equilibrate", type=int, default=1000000,
        help="number of equlibrating collisions (default: 1000000)")
parser.add_argument("-m", "--min_N_atoms", type=int, default=1372,
        help="minimum number of atoms, exact will be ceil((N/4)^(1/3)) "
        "(default: 1372 = 4*7^3)")
parser.add_argument("-p", "--packing", type=float, default=0.3,
        help="the packing fraction, density is p*6/pi (default: 0.3)")
parser.add_argument("--processes", type=int, default=None,
        help="number of processes (cores) to use (default: no. of processors"
        "in the system)")
parser.add_argument("-r", "--repeat", type=int, default=10,
        help="how many times each run should be repeated with random "
        "velocities for statistics (default: 10)")
parser.add_argument("--peek", type=int, nargs="?",
        help="peek at data every PEEK collisions")
parser.add_argument("--jid", default=None, nargs="?",
        help="Job ID to distinguish log files")

args = parser.parse_args()

if args.peek and args.repeat > 1:
    raise Exception("Peeking only works with repeat = 1")

density = args.packing * 6/pi
n_cells = int(ceil( (args.min_N_atoms/4)**(1/3) ))
n_atoms = 4*n_cells**3

"""
    Strings that will be processed by shell in multiple threads.
"""

utcnow = datetime.utcnow()
flavour = str(int(calendar.timegm(utcnow.utctimetuple())*1e6 + utcnow.microsecond))
flavour += "{:06d}".format(randint(0, 999999))
base_name = "{}_{:0.12f}_{}".format(n_atoms, args.packing, flavour) + "_{0:02d}_"

start_configs = [ ("[ -f configs/" + base_name + "0.xml.bz2 ] || dynamod -m 0 "
    "-C {1} -d {2} --i1 0 -r 1 -o configs/" + base_name + "0.xml.bz2")
    .format(run, n_cells, density) for run in range(args.repeat) ]

equilibrated_configs_string = "[ -f configs/" + base_name + "{1}.xml.bz2 ] || " \
    "dynarun configs/" + base_name + "0.xml.bz2 -c {1} -o configs/" + base_name \
    + "{1}.xml.bz2 --out-data-file peeks/" + base_name + "0_{1}.xml.bz2"

simulations_string = "[ -f results/" + base_name + "{1}_{3}.xml.bz2 ] || " \
    "dynarun -L MSD configs/" + base_name + "{1}.xml.bz2 -c {2} -o configs/" \
    + base_name + "{3}.xml.bz2 --out-data-file results/" + base_name \
    + "{1}_{3}.xml.bz2"

if args.peek:
    simulations_string += " --snapshot-events {}".format(args.peek)
    equilibrated_configs_string += " --snapshot-events {}".format(args.peek)

equilibrated_configs = [ equilibrated_configs_string.format(run, args.equilibrate)
    for run in range(args.repeat) ]

simulations = [ simulations_string.format(run, args.equilibrate, args.collisions,
        args.collisions + args.equilibrate) for run in range(args.repeat) ]

"""
    Running the simulations in multiprocess parallel.
"""

if args.processes is None:
    pool = Pool(min(cpu_count(), len(start_configs)))
else:
    pool = Pool(min(cpu_count(), len(start_configs), args.processes))

partial_safe_runner = partial(safe_runner, jid=args.jid)

pool.map(partial_safe_runner, start_configs)
pool.map(partial_safe_runner, equilibrated_configs)
move_peeks(base_name, 0, args.peek)
pool.map(partial_safe_runner, simulations)
move_peeks(base_name, args.equilibrate, args.peek)
