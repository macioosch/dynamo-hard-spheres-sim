#!/usr/bin/env bash

FILES='results/256000_*_3840000000_19200000000.xml.bz2'
OUTPUT='csv/D-vs-N-256000.csv'
#FILES='results/*_219700000_1098500000.xml.bz2 results/*_2097152000_6291456000.xml.bz2'
#OUTPUT='csv/D-vs-N-new.csv'
#FILES='results/1098500_*_219700000_1098500000.xml.bz2'
#OUTPUT='csv/1098500_219700000_1098500000.csv'

if [ -d ~/Dropbox ]; then
    echo "Processing results from Dropbox…"
    ./to_csv.py ~/Dropbox/staż\ 2013/02-hard-spheres/$FILES > $OUTPUT
elif [ -d results ]; then
    echo "Processing local results…"
    ./to_csv.py $FILES > $OUTPUT
else
    echo "No results found!"
    exit 1
fi

head -n -4 $OUTPUT > csv/uniform.csv

#./plot_pressure.gnuplot
