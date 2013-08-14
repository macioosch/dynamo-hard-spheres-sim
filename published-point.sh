#!/usr/bin/env bash

./batch_runner.py -p 0.2617993877991494 -m 108000 -r 8 -e 20000000 -c 80000000 1>runner.out 2>runner.err &

for f in runner.{out,err}; do
    [ -f $f ] && mv $f stdouterr/
done
