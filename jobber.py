#!/usr/bin/python2 -u
from __future__ import division, print_function, unicode_literals

import argparse
from datetime import datetime
from itertools import izip
from os import mkdir, system
from time import sleep

# local imports
from my_helper_functions_bare import *

"""
    Parsing command line agruments.
"""

parser = argparse.ArgumentParser(
        description="Create and submit multiple DynamO jobs.")
parser.add_argument("-n", action='store_true',
        help="create jobs, but don't submit them")
parser.add_argument("-q", action='store_true',
        help="don't wait, submit immidiately")
parser.add_argument("--log", dest='linspace', action='store_const',
        const=my_log_linspace, default=my_linspace,
        help="log scale: equal ratios of subsequent values")
parser.add_argument("--round", action='store_const',
        const=lambda x: int(round(x)), default=lambda x: x,
        help="rounded integer values")
parser.add_argument("--pp", help="parameters to variate, without any dashes")
parser.add_argument("--p0", type=float, help="parameters' minimum values")
parser.add_argument("--p1", type=float, help="parameters' maximum values")
parser.add_argument("--pn", type=int,
        help="numbers of points to compute in each \"dimension\"")
parser.add_argument("args",
        help="other arguments to be sent to batch_runner.py")

args = parser.parse_args()

"""
    batch_runner.py jobs to be submitted
"""

if len(args.pp) == 1:
    args.pp = "-" + args.pp
else:
    args.pp = "--" + args.pp

base_name = "./batch_runner.py {} --jid $JOB_ID {}".format(args.args, args.pp) \
        + " {0} 1>runner-{1:03d}.out 2>runner-{1:03d}.err\n"

batch_runs = [ base_name.format(args.round(p), i)
        for i, p in enumerate(args.linspace(args.p0, args.p1, args.pn)) ]

"""
    Writing job scripts.
"""

dir_name = "jobs/" + datetime.now().isoformat()
mkdir(dir_name)
file_names = [ "{}/{:03d}.sh".format(dir_name, i) for i in xrange(args.pn) ]

for command, file_name in izip(batch_runs, file_names):
    with open(file_name,"w+") as f_out:
        with open("jobs/job-start.sh","r") as f_beginning:
            f_out.write(f_beginning.read())
        f_out.write("echo \"Job $JOB_ID is executed on $HOSTNAME, command: "
                + command + "\"")
        f_out.write(command)
        with open("jobs/job-end.sh","r") as f_end:
            f_out.write(f_end.read())

"""
    Submitting the jobs.
"""
if not args.n:
    for file_name in file_names:
        system("qsub " + file_name)

        if not args.q:
            sleep(1)
            for i in range(29):
                print('.', end='')
                sleep(1)
            print()
else:
    print("Not submitting anything.")
