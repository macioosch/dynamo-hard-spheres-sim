#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function

from sys import argv, stdout
from xml.dom import minidom
import bz2
import csv
import numpy as np

# local imports
from my_helper_functions import my_pressure

varying_parameters = ["pressures_virial", "pressures_collision", "msds_val",
        "msds_diffusion", "times"]
data = { i:[] for i in varying_parameters }
data = dict(data.items() + {"packings": [], "collisions": [], "n_atoms": []}.items())

for input_file in argv[1:]:
    xmldoc = minidom.parse(bz2.BZ2File(input_file))

    packing = float(xmldoc.getElementsByTagName('PackingFraction')[0].attributes['val'].value)
    n_atoms = float(xmldoc.getElementsByTagName('ParticleCount')[0].attributes['val'].value)

    if len(data["packings"]) == 0 or packing != data["packings"][-1] \
            or n_atoms != data["n_atoms"][-1]:
        data["packings"].append(packing)
        data["n_atoms"].append(n_atoms)
        data["collisions"].append(float(xmldoc.getElementsByTagName(
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

stdout_writer = csv.writer(stdout, delimiter=';')
stdout.write("### Data format: packings;densities;collisions;n_atoms;"
        "pressures_virial;pressures_collision;msds_val;msds_diffusion;times"
        "std:pressures_virial;std:pressures_collision;std:msds_val;"
        "std:msds_diffusion;std:times;\n")

for i in xrange(len(data["packings"])):
    stdout_writer.writerow([
        data["packings"][i],
        data["packings"][i]*6.0/np.pi,
        data["collisions"][i],
        data["n_atoms"][i],
        np.mean(data["pressures_virial"][i]),
        np.mean(data["pressures_collision"][i]),
        np.mean(data["msds_val"][i]),
        np.mean(data["msds_diffusion"][i]),
        np.mean(data["times"][i]),
        np.std(data["pressures_virial"][i]),
        np.std(data["pressures_collision"][i]),
        np.std(data["msds_val"][i]),
        np.std(data["msds_diffusion"][i]),
        np.std(data["times"][i])
        ])
