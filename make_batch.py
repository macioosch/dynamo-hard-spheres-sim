#!/usr/bin/env python
from numpy import linspace, pi

base_str = './jobber.py -q --pp "m" --p0 {0:.0f} --p1 {0:.0f} --pn 1 --log '\
        '--round "-p {1:.16f} -r 1 -e {2:.0f} -c {3:.0f}"'

for N in (int(i) for i in 2**linspace(10,20,11)):
    for pf in linspace(0.1,0.9,5)*pi/6:
        print(base_str.format(N, pf, N*12e3, N*6e4))
