#!/usr/bin/env bash

FILES='results/*_219700000_1098500000.xml.bz2 results/*_2097152000_6291456000.xml.bz2'
OUTPUT='csv/D-vs-N-new-pretty.csv'
#FILES='results/1098500_*_219700000_1098500000.xml.bz2'
#OUTPUT='csv/1098500_219700000_1098500000-pretty.csv'

if [ -d ~/Dropbox ]; then
    echo "Processing results from Dropbox…"
    ./to_csv_pretty.py ~/Dropbox/staż\ 2013/02-hard-spheres/$FILES > $OUTPUT
elif [ -d results ]; then
    echo "Processing results from Dropbox…"
    ./to_csv_pretty.py $FILES > $OUTPUT
else
    echo "No results found!"
    exit 1
fi

tail -n +20 $OUTPUT | head -n 49 > csv/uniform.csv

#./plot_pressure.gnuplot
