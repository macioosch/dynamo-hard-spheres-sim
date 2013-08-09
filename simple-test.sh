#!/usr/bin/env bash
dynamod -m 0 -C 7 -d 1.0 --i1 0 -r 1 -o config.start.xml
dynarun config.start.xml -c 600000 -o config.end.xml -L MSD
