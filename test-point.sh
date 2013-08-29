#!/usr/bin/env bash

./batch_runner.py --processes 5 -r 10 -m 1000 -e 200000 -c 800000 1>runner.out 2>runner.err &

for f in runner.{out,err}; do
    [ -f $f ] && mv $f stdouterr/
done
