#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function

from math import pi
from sys import argv
from xml.dom import minidom
import bz2

# local imports
from my_helper_functions_bare import *

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

param="pressures_collision"

for i in xrange(len(data["packings"])):
    if data["msds_diffusion"][i][0] is None:
        continue
    print("d = {:.6f}:\t{:2d} runs,\trelative error*1e6: {:9.6f}".format(
        data["packings"][i]*6.0/pi, len(data[param][i]),
        1e6 * my_means_std(data[param][i]) / my_mean(data[param][i])))
