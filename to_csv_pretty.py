#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function

from math import ceil, floor, log10, pi
from sys import argv, stdout
from xml.dom import minidom
import bz2
import csv

# local imports
from my_helper_functions_bare import *

def pretty_mean_std(data):
    return uncertain_number_string(my_mean(data), my_means_std(data))

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
"""
stdout.write("### Data format: packings\tdensities\tcollisions\tn_atoms\t"
        "pressures_virial\tpressures_collision\tmsds_val\tmsds_diffusion\t"
        "times\n")
"""
stdout.write("\multicolumn{1}{c}{$\zeta$}\t\multicolumn{1}{c}{$Z_{MD}$}\t"
        "\multicolumn{1}{c}{$\Delta Z_{MD}$}\n")

for i in xrange(len(data["packings"])):
    if data["msds_diffusion"][i][0] is None:
        continue
    """
    stdout_writer.writerow([
        "{:.9f}".format(data["packings"][i]),
        "{:.9f}".format(data["packings"][i]*6.0/pi),
        data["collisions"][i],
        data["n_atoms"][i],
        pretty_mean_std(data["pressures_virial"][i]),
        pretty_mean_std(data["pressures_collision"][i]),
        pretty_mean_std(data["msds_val"][i]),
        pretty_mean_std(data["msds_diffusion"][i]),
        pretty_mean_std(data["times"][i])
        ])
    """
    stdout_writer.writerow([
        "{:.9f}".format(data["packings"][i]),
        "{:.9f}".format(my_mean(data["pressures_collision"][i])),
        "{:.9f}".format(my_means_std(data["pressures_collision"][i]))
        ])
