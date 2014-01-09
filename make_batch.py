#!/usr/bin/env python2
from numpy import ceil, linspace, pi

base_str = './jobber.py -q --pp "m" --p0 {0:.0f} --p1 {0:.0f} --pn 1 '\
        '--round "-p {1:.16f} -r 1 -e {2:.0f} -c {3:.0f}"'

N_min = 10
N_sizes = 7

for index, i in enumerate(2**linspace(N_min, N_min + N_sizes - 1, N_sizes)):
    N = int(ceil((i/4)**(1/3.))**3*4)
    for pf in linspace(0.1, 0.1, 1)*pi/6:
        for _ in range(2**(N_sizes - index - 1)):
            print(base_str.format(N, pf, N*12e3, N*6e4))

#N_max = 18
#for index, i in enumerate(2**linspace(N_min + N_sizes, N_max, N_max - N_min - N_sizes + 1)):
#    N = int(ceil((i/4)**(1/3.))**3*4)
#    for pf in linspace(0.2, 0.8, 4)*pi/6:
#        print(base_str.format(N, pf, N*12e3, N*6e4))
