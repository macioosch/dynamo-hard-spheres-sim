#!/usr/bin/env bash

## density 0.537 +- 0.005, that is packing:
./jobber.py --pp "p" --p0 0.2759365547403035 --p1 0.2864085302522695 --pn 18 "-m 1098500 -r 8 -e 219700000 -c 878800000"

## density 0.0785 +- 0.01, that is packing:
#./jobber.py --pp "p" --p0 0.04005530633326986 --p1 0.04214970143566305 --pn 10 "-m 1098500 -r 8 -e 219700000 -c 878800000"


## test job:
#./jobber.py --pp "m" --p0 1024 --p1 4096 --pn 3 --log --round "-p 0.2617993877991494 -r 4 -e 1197000 -c 2788000"
