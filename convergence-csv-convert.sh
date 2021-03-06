#!/usr/bin/env bash
time ./convergence-csv.py 256000 2560000000 > csv/convergence-256000.csv

#time ./convergence-csv.py 256000 500000000 > csv/convergence-256000.csv
#time ./convergence-csv.py 500000 1000000000 > csv/convergence-500000.csv
#time ./convergence-csv.py 1000188 2000000000 > csv/convergence-1000188.csv

cd csv/
source convergence-densities.sh

cd ..
./convergence-plot.py
