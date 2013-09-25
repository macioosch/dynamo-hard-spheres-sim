#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function

from math import pi
from sys import argv, stdout
from xml.dom import minidom
import bz2
import csv

# local imports
from my_helper_functions_bare import *

varying_parameters = ["pressures_virial", "pressures_collision", "msds_val",
        "msds_diffusion", "times"]
data = { i:[] for i in varying_parameters }
data = dict(data.items() + {"packings": [], "collisions": [], "n_atoms": []}.items())

for input_file in argv[1:]:
    xmldoc = minidom.parse(bz2.BZ2File(input_file))

    packing = float(xmldoc.getElementsByTagName('PackingFraction')[0].attributes['val'].value)
    n_atoms = int(xmldoc.getElementsByTagName('ParticleCount')[0].attributes['val'].value)

    if len(data["packings"]) == 0 or packing != data["packings"][-1] \
            or n_atoms != data["n_atoms"][-1]:
        data["packings"].append(packing)
        data["n_atoms"].append(n_atoms)
        data["collisions"].append(int(xmldoc.getElementsByTagName(
                'Duration')[0].attributes['TwoParticleEvents'].value))
        for parameter in varying_parameters:
            data[parameter].append([])

    data["times"][-1].append(float(
        xmldoc.getElementsByTagName('Duration')[0].attributes['Time'].value))
    data["pressures_virial"][-1].append(float(
        xmldoc.getElementsByTagName('Pressure')[0].attributes['Avg'].value))
    data["pressures_collision"][-1].append(my_pressure(data["n_atoms"][-1],
        data["collisions"][-1], data["times"][-1][-1]))
    try:
        data["msds_val"][-1].append(float(
            xmldoc.getElementsByTagName('Species')[0].attributes['val'].value))
        data["msds_diffusion"][-1].append(float(
            xmldoc.getElementsByTagName('Species')[0].attributes['diffusionCoeff'].value))
    except:
        data["msds_val"][-1].append(None)
        data["msds_diffusion"][-1].append(None)

stdout_writer = csv.writer(stdout, delimiter='\t')
stdout.write("### Data format: packings\tdensities\tcollisions\tn_atoms\t"
        "pressures_virial\tpressures_collision\tmsds_val\tmsds_diffusion\ttimes\t"
        "std:pressures_virial\tstd:pressures_collision\tstd:msds_val\t"
        "std:msds_diffusion\tstd:times\n")

for i in xrange(len(data["packings"])):
    if data["msds_diffusion"][i][0] is None:
        continue
    stdout_writer.writerow([
        "{:.9f}".format(data["packings"][i]),
        "{:.9f}".format(data["packings"][i]*6.0/pi),
        data["collisions"][i],
        data["n_atoms"][i],
        "{:.9f}".format(my_mean(data["pressures_virial"][i])),
        "{:.9f}".format(my_mean(data["pressures_collision"][i])),
        "{:.9f}".format(my_mean(data["msds_val"][i])),
        "{:.9f}".format(my_mean(data["msds_diffusion"][i])),
        "{:.9f}".format(my_mean(data["times"][i])),
        "{:.9f}".format(my_means_std(data["pressures_virial"][i])),
        "{:.9f}".format(my_means_std(data["pressures_collision"][i])),
        "{:.9f}".format(my_means_std(data["msds_val"][i])),
        "{:.9f}".format(my_means_std(data["msds_diffusion"][i])),
        "{:.9f}".format(my_means_std(data["times"][i]))
        ])
