#!/usr/bin/env bash
for d in 0.{1..9..2}; do
    grep '###' convergence.csv > convergence-${d}.csv
    grep ${d}00000000 convergence.csv >> convergence-${d}.csv
done