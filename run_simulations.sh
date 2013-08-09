#!/bin/bash
for f in config.start.*.equilibrated.xml
do
    test -f ${f%.equilibrated.xml}.output.xml || \
        dynarun $f -c 1000000 -o /dev/null --out-data-file ${f%.equilibrated.xml}.output.xml -L MSD
done
