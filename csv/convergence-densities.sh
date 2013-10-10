#!/usr/bin/env bash
for n in 256000 500000 1000188; do
    for d in 0.{1..9..2}; do
        grep '###' convergence-${n}.csv > convergence-${n}-${d}.csv
        grep -F ${d}00000000 convergence-${n}.csv >> convergence-${n}-${d}.csv
    done
done
for f in convergence-500000*.csv; do
    grep -v 1083333333 $f | grep -v 1025000000 | sponge $f
done
