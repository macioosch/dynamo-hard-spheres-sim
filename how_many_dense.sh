#!/usr/bin/env bash
./how_many_stats.py results/1098500_*_219700000_1098500000.xml.bz2 | sed 's/^[^\t]*\t\([0-9]* runs\)/\1/' | sort | uniq -c
