#!/usr/bin/env python3
import argparse
from math import ceil, pi
from multiprocessing import Pool
from os import system, getpid
from pprint import pprint

def safe_runner(command):
    try:
        system(command + ">/dev/null")
    except:
        print("Oops! Command '{}' didn't work.".format(command))
    print("Command '{}' done by process {}.".format(command, getpid()))

"""
    Parsing command line agruments.
"""

parser = argparse.ArgumentParser(
        description="Run multiprocess DynamO simulations with given "
        "parameters.")
parser.add_argument("-p", "--packing", type=float, default=0.3,
        help="the packing fraction, density is p*6/pi (default: 0.3)")
parser.add_argument("-M", "--min_N_atoms", type=int, default=1372,
        help="minimum number of atoms, exact will be ceil((N/4)^(1/3)) "
        "(default: 1372 = 4*7^3)")
parser.add_argument("-r", "--repeat", type=int, default=10,
        help="how many times each run should be repeated with random "
        "velocities for statistics (default: 10)")
parser.add_argument("-e", "--equilibrate", type=int, default=1000000,
        help="number of equlibrating collisions (default: 1000000)")
parser.add_argument("-c", "--collisions", type=int, default=1000000,
        help="number of simulated collisions after equlibrating (default: "
        "1000000)")

args = parser.parse_args()

density = args.packing * 6/pi
n_cells = ceil( (args.min_N_atoms/4)**(1/3) )
n_atoms = 4*n_cells**3

"""
    Strings that will be processed by shell in multiple threads.
"""

base_name = "{}_{:0.12f}".format(n_atoms, args.packing) + "_{0:02d}_"

start_configs = [ ("[ -f configs/" + base_name + "0.xml ] || dynamod -m 0 "
    "-C {1} -d {2} --i1 0 -r 1 -o configs/" + base_name + "0.xml")
    .format(run, n_cells, density) for run in range(args.repeat) ]

equilibrated_configs = [ ("[ -f configs/" + base_name + "{1}.xml ] || "
    "dynarun configs/" + base_name + "0.xml -c {1} -o configs/" + base_name
    + "{1}.xml -E --out-data-file /dev/null").format(run, args.equilibrate)
    for run in range(args.repeat) ]

simulations = [ ("[ -f results/" + base_name + "{1}_{3}.xml ] || "
    "dynarun configs/" + base_name + "{1}.xml -c {2} -o configs/" + base_name +
    "{3}.xml --out-data-file results/" + base_name + "{1}_{3}.xml").format(run,
        args.equilibrate, args.collisions, args.collisions + args.equilibrate)
    for run in range(args.repeat) ]

"""
    Running the simulations in multiprocess parallel.
"""

pool = Pool()
pool.map(safe_runner, start_configs)
pool.map(safe_runner, equilibrated_configs)
pool.map(safe_runner, simulations)
