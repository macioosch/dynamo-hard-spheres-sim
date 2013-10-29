#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function

from glob import glob
from uncertainties import numpy as unp, ufloat
from scipy.optimize import curve_fit
from sys import stderr, stdout
from xml.dom import minidom
import bz2
import csv
import matplotlib.pyplot as plt
import numpy as np
import progressbar as pb

# local imports
from my_helper_functions_bare import *
from my_helper_functions import *

varying_parameters = ["pressures_virial", "pressures_collision", "msds_val",
        "msds_diffusion", "collisions", "times"]
data = { i:[] for i in varying_parameters }
data = dict(data.items() + {"packings": [], "collisions": [], "n_atoms": []}.items())

#input_files = sorted(glob(u"/home/mc/Dropbox/staż 2013/02-hard-spheres/"
#        u"results/1098500_*_219700000_1098500000.xml.bz2"))

# the D(N) results
input_files = []
base_path = u"/home/mc/Dropbox/staż 2013/02-hard-spheres/results/"

widgets = ['Finding files: ', pb.Counter(), ' done (', pb.Percentage(),
    '), ', pb.ETA(), ' ', pb.Bar()]
pbar = pb.ProgressBar(widgets=widgets, maxval=55)
pbar.start()

for i_index, i in enumerate(2**np.linspace(10,20,11)):
    N = int(np.ceil((i/4.)**(1/3.))**3*4)
    for pf_index, pf in enumerate(np.linspace(0.1,0.9,5)*np.pi/6):
        input_files += glob(base_path \
                + u"{:.0f}_{:.12f}_*_{:.0f}_{:.0f}.xml.bz2".format(
                    N, pf, N*12e3, N*12e3 + N*6e4))
        pbar.update(1 + pf_index + 5*i_index)

pbar.finish()

stdout_writer = csv.writer(stdout, delimiter='\t')
stdout.write("### Data format: n_atoms\tmsds_diffusion\tstd:msds_diffusion\n")

widgets = ['Processing files: ', pb.Counter(), ' done (', pb.Percentage(),
    '), ', pb.ETA(), ' ', pb.Bar()]
pbar = pb.ProgressBar(widgets=widgets)

for input_file in pbar(input_files):
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

"""
d = (6/np.pi) * np.array([np.mean(i) for i in data["packings"]])
Z = np.array([np.mean(i) for i in data["pressures_collision"]])
P = np.array([np.mean(i) for i in data["pressures_virial"]])
plt.figure(1)

#plt.plot((Z)/(P/d), 'o')

plt.plot(data["packings"], Z/(P/d)-1, 'o')
plt.xlabel("Packing fraction")
plt.ylabel("Pressure")
plt.legend(["Z","P"])
"""
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
def fit_func(x, y0, a):
    return y0 - a*x

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

        stdout.write("###\n### Density: {:.3f}\n###\n".format(packing*6/np.pi))
        n_ints = [ int(n) for n in ns ]

        # the normal csv version:
        stdout_writer.writerows(zip(n_ints, ds, er))
        ## the pretty version:
        #unc_strings = [ uncertain_number_string(d, e) for d, e in zip(ds, er) ]
        #stdout_writer.writerows(zip(n_ints, unc_strings))

        plt.subplot(subplot)
        plt.ylabel("$D$")
        if subplot in {324, 325}:
            plt.xlabel("$N^{-1/3}$")
        #plt.xscale("log")
        #plt.yscale("log")
        plt.xlim([0, 0.1])

        # Curve fitting:
        popt, pcov = curve_fit(fit_func, 1./ns**(1/3.), ds, [0.4, 0.1],
                er/np.sqrt(len(er)))
        stderr.write("density: {}, y0 = {}, a = {}\n".format(packing*6/np.pi,
                uncertain_number_string(popt[0], np.sqrt(pcov[0][0])),
                uncertain_number_string(popt[1], np.sqrt(pcov[1][1]))))
        xs = np.linspace(0, 0.1, 100)
        plt.plot(xs, fit_func(xs, *popt))

        plt.errorbar(1.0/ns**(1/3.), ds, fmt='.', yerr=er/np.sqrt(len(er)))

        plt.ylim(popt[0] * np.array([0.90, 1.02]))
        
        plt.legend(["$\\rho\\sigma^3 =$ ${:.1f},$".format(packing*6/np.pi)
                + " $D_{inf}"+"$ $=$ ${}$".format(uncertain_number_string(
                    popt[0], np.sqrt(pcov[0][0])))], loc="lower left")

        #plt.errorbar(1.0/ns, ds/ds[-1], fmt='-o', yerr=er / np.sqrt(len(er)) / ds[-1])
        #legend_names.append(packing)
#plt.ylabel("Diffusion coefficient relative to the \"precise\" value: "
#        "d(N) / d(N=1098500)")
#plt.legend(legend_names, loc='lower left')

plt.show()
