#!/usr/bin/env python2
from numpy import linspace
from os import system

for i in linspace(0.1, 1.4, 27):
    system("dynamod -m 0 -C 7 -d {0} --i1 0 -r 1 -o config.start.{0:.5f}.xml".format(i))
