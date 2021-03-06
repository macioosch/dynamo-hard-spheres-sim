#!/usr/bin/env bash
# NOW THIS SCRIPT MAY BE EXECUTED AUTOMATICALLY
# !  EDIT WITH CAUTION  !

## density 0.537 +- 0.005, C/N = 6e4, 1M:
./jobber.py -q --pp "p" --p0 0.2759365547403035 --p1 0.2864085302522695 --pn 5 "-m 1098500 -r 1 -e 16477500000 -c 65910000000" &>/dev/null

## density 0.537 +- 0.005, C/N = 6e4, 256k:
#./jobber.py -q --pp "p" --p0 0.2759365547403035 --p1 0.2864085302522695 --pn 25 "-m 256000 -r 1 -e 3840000000 -c 15360000000" &>/dev/null

## density 0.55..0.70, C/N = 6e4, 256k:
#./jobber.py -q --pp "p" --p0 0.2879793265790644 --p1 0.3665191429188092 --pn 4 "-m 256000 -r 1 -e 3840000000 -c 15360000000" &>/dev/null

## density 0.537 +- 0.005:
#./jobber.py -q --pp "p" --p0 0.2759365547403035 --p1 0.2864085302522695 --pn 25 "-m 1098500 -r 1 -e 219700000 -c 878800000" &>/dev/null

## density 0.537 +- 0.005, points in between:
#./jobber.py -q --pp "p" --p0 0.27615472089680276 --p1 0.2861903640957702 --pn 24 "-m 1098500 -r 1 -e 219700000 -c 878800000" &>/dev/null

## density 0.0785 +- 0.01:
#./jobber.py --pp "p" --p0 0.04005530633326986 --p1 0.04214970143566305 --pn 10 "-m 1098500 -r 8 -e 219700000 -c 878800000"

## test job:
#./jobber.py -q --pp "p" --p0 0.2759365547403035 --p1 0.2864085302522695 --pn 3 "-m 1000 -r 2 -e 200000 -c 800000"
