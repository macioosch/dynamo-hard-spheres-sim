#!/usr/bin/env bash

./batch_runner.py -p 0.2617993877991494 -m 1098500 -r 8 -e 219700000 -c 878800000 1>runner.out 2>runner.err &

for f in runner.{out,err}; do
    [ -f $f ] && mv $f stdouterr/
done
