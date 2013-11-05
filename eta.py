#!/usr/bin/env python2
import datetime
import fileinput
import pickle
import re

regexp_time = ((86400," ([0-9]+)d"), (3600," ([0-9]+)hr"),
        (60," ([0-9]+)min"), (1," ([0-9]+)s, "))
regexp_events = "Events ([0-9]+)k,"

now = datetime.datetime.now()
etas = []

for line in fileinput.input():
    eta = 0
    for seconds, pattern in regexp_time:
        match = re.search(pattern, line)
        if match:
            eta += seconds*int(match.group(1))
    etas.append(eta)
    collisions = 1000*int(re.search(regexp_events, line).group(1))
    print("{:7.3f} h left, {:4.2e} collisions done, finish: {}".format(
            eta/3600., collisions, now + datetime.timedelta(seconds=eta)))

with open("eta.pickle", "w+") as output_file:
    pickle.dump(etas, output_file)
