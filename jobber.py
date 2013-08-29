#!/usr/bin/env python2
from __future__ import division

import argparse
from datetime import datetime
from itertools import izip
from os import system, mkdir
from pprint import pprint

def my_linspace(x0, x1, xc):
    return [ x0 + (x1-x0)*i/(xc-1) for i in xrange(xc) ]

"""
    Parsing command line agruments.
"""

parser = argparse.ArgumentParser(
        description="Create and submit many DynamO jobs.")
parser.add_argument("--p0", type=float, default=0.2,
        help="the packing fraction, density is p*6/pi (default: 0.2)")
parser.add_argument("--p1", type=float, default=0.3,
        help="the packing fraction, density is p*6/pi (default: 0.3)")
parser.add_argument("--pc", type=int, default=10,
        help="number of points to compute (default: 10)")
parser.add_argument("args", help="constant arguments to be sent to batch_runner.py")

args = parser.parse_args()

"""
    batch_runner.py jobs to be submitted
"""

base_name = "./batch_runner.py {} --jid $JOB_ID ".format(args.args) \
        + "-p {0} 1>runner-{1:03d}.out 2>runner-{1:03d}.err\n"

batch_runs = [ base_name.format(p, i)
        for i, p in enumerate(my_linspace(args.p0, args.p1, args.pc)) ]

"""
    Writing job scripts.
"""

dir_name = "jobs/" + datetime.now().isoformat()
mkdir(dir_name)
file_names = [ dir_name + "/{:03d}.sh".format(i) for i in xrange(args.pc) ]

for command, file_name in izip(batch_runs, file_names):
    with open(file_name,"w+") as f_out:
        with open("jobs/job-start.sh","r") as f_beginning:
            f_out.write(f_beginning.read())
        f_out.write("echo Job $JOB_ID is executed on $HOSTNAME, command: " + command)
        f_out.write(command)
        with open("jobs/job-end.sh","r") as f_end:
            f_out.write(f_end.read())

"""
    Submitting the jobs.
"""

for file_name in file_names:
    system("qsub " + file_name)
