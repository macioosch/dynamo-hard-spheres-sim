#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function, unicode_literals

from uncertainties import unumpy as unp, ufloat
from xml.dom import minidom
import bz2
import csv
import glob
import matplotlib.pyplot as plt
import numpy as np

# local imports
from my_helper_functions import *

varying_parameters = ["pressures_virial", "pressures_collision", "msds_val",
        "msds_diffusion", "times"]
data = { i:[] for i in varying_parameters }
data = dict(data.items() + {"packings": [], "collisions": [], "n_atoms": []}.items())

input_files = sorted(glob.glob("/home/mc/Dropbox/staż 2013/02-hard-spheres/"
        "results/1098500_*_219700000_1098500000.xml.bz2"))
print("Got {} files.".format(len(input_files)))

for input_file in input_files:
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
        data["msds_diffusion"][-1].append(float(xmldoc.getElementsByTagName(
            'Species')[0].attributes['diffusionCoeff'].value))
    except:
        data["msds_val"][-1].append(None)
        data["msds_diffusion"][-1].append(None)

#graphed_parameter = data["pressures_collision"]
graphed_parameter = data["pressures_virial"]
plt.figure(0)
up = unp.uarray([np.mean(i) for i in graphed_parameter],
    [np.std(i)/np.sqrt(len(i)) for i in graphed_parameter])

#uplot(np.array(data["packings"]), up)
#plt.ylabel("Pressure p")

DX = nufd(np.array(data["packings"])).toarray()

#x1, p1 = uderivative_oh4(np.array(data["packings"]), up)
#uplot(x1, p1)
#plt.legend(["O(h^4) method", "Array method"])
#uplot(np.array(data["packings"]), np.dot(DX, up))
#plt.ylabel("First derivative of pressure: dp/dn")

#x2, p2 = uderivative_2_oh4(np.array(data["packings"]), up)
#uplot(x2, p2)
#plt.legend(["O(h^4) method", "Array method"])
uplot(np.array(data["packings"]), np.dot(DX, np.dot(DX, up)))
plt.ylabel("Second derivative of pressure: d2p/dn2")

plt.xlabel("Packing fraction n")
plt.xlim(0.275, 0.287)

## plot of standard deviations:
#plt.plot(data["packings"], [np.std(i) / (np.sqrt(len(i))*np.mean(i))
#    for i in data["pressures_collision"]], 'o')

plt.show()
