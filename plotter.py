#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function, unicode_literals

from xml.dom import minidom
import bz2
import glob
import matplotlib.pyplot as plt
import numpy as np

# local imports
from my_pressure import my_pressure

varying_parameters = ["pressures_virial", "pressures_collision", "msds_val",
        "msds_diffusion", "collisions", "times"]
data = { i:[] for i in varying_parameters }
data = dict(data.items() + {"packings": [], "collisions": [], "N_atoms": []}.items())

input_files = sorted(glob.glob("/home/mc/Dropbox/staż 2013/02-hard-spheres/"
        "results/1098500_*_219700000_1098500000.xml.bz2"))
print("Got {} files.".format(len(input_files)))

for input_file in input_files:
    xmldoc = minidom.parse(bz2.BZ2File(input_file))

    packing = float(xmldoc.getElementsByTagName('PackingFraction')[0].attributes['val'].value)

    if len(data["packings"]) == 0 or packing != data["packings"][-1]:
        data["packings"].append(packing)
        for parameter in varying_parameters:
            data[parameter].append([])

    data["collisions"].append(float(xmldoc.getElementsByTagName(
            'Duration')[0].attributes['TwoParticleEvents'].value))
    data["N_atoms"].append(float(xmldoc.getElementsByTagName(
            'ParticleCount')[0].attributes['val'].value))

    data["pressures_virial"][-1].append(float(
        xmldoc.getElementsByTagName('Pressure')[0].attributes['Avg'].value))
    data["times"][-1].append(float(
        xmldoc.getElementsByTagName('Duration')[0].attributes['Time'].value))
    data["pressures_collision"][-1].append(my_pressure(data["N_atoms"][-1], data["collisions"][-1],
        data["times"][-1][-1]))
    try:
        data["msds_val"][-1].append(float(
            xmldoc.getElementsByTagName('Species')[0].attributes['val'].value))
        data["msds_diffusion"][-1].append(float(
            xmldoc.getElementsByTagName('Species')[0].attributes['diffusionCoeff'].value))
    except:
        data["msds_val"][-1].append(None)
        data["msds_diffusion"][-1].append(None)

pub_data = np.genfromtxt('published-values.csv', delimiter=' ')

plt.figure(1)
#plt.plot(data["packings"], [np.mean(i) for i in data["pressures_collision"]], '-o',
#        pub_data.T[0] * np.pi/6, pub_data.T[1], '.')
#plt.plot([np.std(i)/np.mean(i) for i in data["pressures_collision"]], 
#        [np.std(i)/np.mean(i) for i in data["pressures_virial"]], 'o')
plt.plot(data["packings"], [np.mean(i) for i in data["pressures_collision"]], '-o')
plt.xlabel("Packing fraction")
plt.ylabel("Pressure")
"""
plt.figure(2)
plt.semilogy(pub_data.T[0] * np.pi/6,
        abs(ZMD[:len(pub_data.T[1])] - (pub_data.T[1] - 1.0)),
        '-o')
plt.xlabel("Packing fraction")
plt.ylabel("Pressure difference")

plt.figure(3)
plt.semilogy(packings, msds_val, '-o')
plt.semilogy(packings, msds_diffusion, '-o')
plt.xlabel("Packing fraction")
plt.ylabel("MSD, diffusion coef.")
plt.legend(["MSD","diffusion coef."])
"""
plt.show()
