#!/bin/bash
for f in config.start.*.xml
do
    test -f ${f%.xml}.equilibrated.xml || \
        dynarun $f -c 1000000 -o ${f%.xml}.equilibrated.xml --out-data-file /dev/null
done
