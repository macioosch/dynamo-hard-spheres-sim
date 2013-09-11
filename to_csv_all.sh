#!/usr/bin/env bash

FILES='results/1098500_*_219700000_1098500000.xml.bz2'
OUTPUT='csv/1098500_219700000_1098500000.csv'

if [ -d ~/Dropbox ]; then
    #PREFIX='~/Dropbox/staż 2013/02-hard-spheres/'
    ./to_csv.py ~/Dropbox/staż\ 2013/02-hard-spheres/$FILES > $OUTPUT
elif [ -d results ]; then
    ./to_csv.py $FILES > $OUTPUT
else
    print "No results found!"
    exit 1
fi

tail -n +15 $OUTPUT | head -n 25 > csv/uniform.csv

./plot_pressure.gnuplot
