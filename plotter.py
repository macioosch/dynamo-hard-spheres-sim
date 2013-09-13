#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function, unicode_literals

from uncertainties import numpy as unp, ufloat
from xml.dom import minidom
import bz2
import glob
import matplotlib.pyplot as plt
import numpy as np

# local imports
from my_helper_functions import my_pressure

varying_parameters = ["pressures_virial", "pressures_collision", "msds_val",
        "msds_diffusion", "collisions", "times"]
data = { i:[] for i in varying_parameters }
data = dict(data.items() + {"packings": [], "collisions": [], "n_atoms": []}.items())

#input_files = sorted(glob.glob("/home/mc/Dropbox/staż 2013/02-hard-spheres/"
#        "results/1098500_*_219700000_1098500000.xml.bz2"))
input_files = sorted(glob.glob("/home/mc/Dropbox/staż 2013/02-hard-spheres/"
        "results/*_219700000_1098500000.xml.bz2"))
print("Got {} files.".format(len(input_files)))

for input_file in input_files:
    xmldoc = minidom.parse(bz2.BZ2File(input_file))

    packing = float(xmldoc.getElementsByTagName('PackingFraction')[0].attributes['val'].value)
    n_atoms = float(xmldoc.getElementsByTagName('ParticleCount')[0].attributes['val'].value)

    if len(data["packings"]) == 0 or packing != data["packings"][-1] \
            or n_atoms != data["n_atoms"][-1]:
        data["packings"].append(packing)
        data["n_atoms"].append(n_atoms)
        for parameter in varying_parameters:
            data[parameter].append([])

    data["collisions"].append(float(xmldoc.getElementsByTagName(
            'Duration')[0].attributes['TwoParticleEvents'].value))

    data["pressures_virial"][-1].append(float(
        xmldoc.getElementsByTagName('Pressure')[0].attributes['Avg'].value))
    data["times"][-1].append(float(
        xmldoc.getElementsByTagName('Duration')[0].attributes['Time'].value))
    data["pressures_collision"][-1].append(my_pressure(data["n_atoms"][-1], data["collisions"][-1],
        data["times"][-1][-1]))
    try:
        data["msds_val"][-1].append(float(
            xmldoc.getElementsByTagName('Species')[0].attributes['val'].value))
        data["msds_diffusion"][-1].append(float(
            xmldoc.getElementsByTagName('Species')[0].attributes['diffusionCoeff'].value))
    except:
        data["msds_val"][-1].append(None)
        data["msds_diffusion"][-1].append(None)

d = (6/np.pi) * np.array([np.mean(i) for i in data["packings"]])
Z = np.array([np.mean(i) for i in data["pressures_collision"]])
P = np.array([np.mean(i) for i in data["pressures_virial"]])
plt.figure(1)

plt.plot((Z-1)/(P/d-1), 'o')

#plt.plot(data["packings"], Z, 'o')
#plt.plot(data["packings"], P/d, 'o')
#plt.xlabel("Packing fraction")
#plt.ylabel("Pressure")
#plt.legend(["Z","P"])

"""
pub_data = np.genfromtxt('published-values.csv', delimiter=' ')

plt.figure(1)
plt.plot(data["packings"], [np.mean(i) for i in data["pressures_collision"]], '-o',
        pub_data.T[0] * np.pi/6, pub_data.T[1], '.')
plt.xlabel("Packing fraction")
plt.ylabel("Pressure")
"""
"""
plt.figure(2)
plt.semilogy(pub_data.T[0] * np.pi/6,
        abs(ZMD[:len(pub_data.T[1])] - (pub_data.T[1] - 1.0)),
        '-o')
plt.xlabel("Packing fraction")
plt.ylabel("Pressure difference")

plt.figure(3)
plt.plot(data["packings"], [np.mean(i) for i in data["msds_diffusion"]], '-o')
plt.xlabel("Packing fraction")
plt.ylabel("Diffusion coefficient")
"""
"""
ax = plt.figure(4)
graphed_parameter = "msds_diffusion"
legend_names = []
for packing, subplot in zip(np.linspace(0.1, 0.9, 5) * np.pi/6,
        [321, 322, 323, 324, 325]):
    ns = [ n for n, p in zip(data["n_atoms"], data["packings"])
            if abs(p/packing - 1.0) < 1e-4 ]
    ds = [ np.mean(d) for d, p in zip(data[graphed_parameter], data["packings"])
            if abs(p/packing - 1.0) < 1e-4 ]
    er = [ np.std(d) for d, p in zip(data[graphed_parameter], data["packings"])
            if abs(p/packing - 1.0) < 1e-4 ]
    if len(ns) > 1:
        ns, ds, er = np.array(sorted(zip(ns, ds, er))).T

        plt.subplot(subplot)
        plt.title("Packing fraction: {}".format(packing))
        plt.ylabel("Diffusion coefficient")
        if subplot in {324, 325}:
            plt.xlabel("1/N")
        plt.xscale("log")
        plt.errorbar(1.0/ns, ds, fmt='.', yerr=er/np.sqrt(len(er)))
        
        #plt.errorbar(1.0/ns, ds/ds[-1], fmt='-o', yerr=er / np.sqrt(len(er)) / ds[-1])
        #legend_names.append(packing)
#plt.ylabel("Diffusion coefficient relative to the \"precise\" value: "
#        "d(N) / d(N=1098500)")
#plt.legend(legend_names, loc='lower left')
"""

plt.show()
