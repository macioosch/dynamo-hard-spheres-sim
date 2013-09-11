#!/usr/bin/env python2
from __future__ import division
from re import search
from sys import stdin

# local imports
from my_helper_functions_bare import *

lines = stdin.readlines()
matches_maybe = [ search(
    "[\t ]([0-9]+) runs,[\t ]+relative error\*1e6: +([0-9\.]+)", l)
    for l in lines ]
matches = [ m.groups() for m in matches_maybe if m ]
runs = dict()

for match in matches:
    r = int(match[0])
    if not r in runs:
        runs[r] = []
    runs[r].append(float(match[1]))

for r, s in sorted(runs.iteritems(), key=lambda x: x[0]):
    mean = my_mean(s)
    err = my_std(s)
    print("For {:2d} runs ({:2d} points) the relative error *1e6 is {:6.3f} +/- {:5.3f} "
        "({:6.3f} ..{:6.3f})".format(r, len(s), mean, err, mean-err, mean+err))
