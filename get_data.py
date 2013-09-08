#!/usr/bin/env python2

from pprint import pprint
from xml.dom import minidom
import bz2
import glob
import matplotlib.pyplot as plt
import numpy as np
import re

# local imports
from my_helper_functions import my_pressure

packings = []
pressures = []
#msds_val = []
#msds_diffusion = []
collisions = []
times = []
N_atoms = []

result_name_regexp = "results/([0-9]+)_(0\.[0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)\.xml\.bz2"

for input_file in sorted(glob.glob("results/1098500_*.xml.bz2")):
    """
    file_tmp_str = re.sub("results/", "", input_file)
    file_tmp_str = re.sub("\.xml\.bz2", "", file_tmp_str)
    file_params = re.split("_", file_tmp_str)
    del file_params[2]
    """

    xmldoc = minidom.parse(bz2.BZ2File(input_file))
    packings.append( float( 
        xmldoc.getElementsByTagName('PackingFraction')[0].attributes['val'].value))
    pressures.append(float(
        xmldoc.getElementsByTagName('Pressure')[0].attributes['Avg'].value))
    #msds_val.append(float(
    #    xmldoc.getElementsByTagName('Species')[0].attributes['val'].value))
    #msds_diffusion.append(float(
    #    xmldoc.getElementsByTagName('Species')[0].attributes['diffusionCoeff'].value))
    collisions.append(float(
        xmldoc.getElementsByTagName('Duration')[0].attributes['TwoParticleEvents'].value))
    times.append(float(
        xmldoc.getElementsByTagName('Duration')[0].attributes['Time'].value))
    N_atoms.append(float(
        xmldoc.getElementsByTagName('ParticleCount')[0].attributes['val'].value))

pressures = pressure(np.array(N_atoms), np.array(collisions), np.array(times))
mean_p = np.mean(pressures)
std_p = np.std(pressures)
print("Pressure: {:.6f} +- {:.6f} ({:.2e})".format(mean_p, std_p, std_p/mean_p))

#pub_data = np.genfromtxt('published-values.csv', delimiter=' ')
"""
plt.figure(1)
plt.plot(packings, ZMD, '-o', packings, pressures, '-o')
plt.xlabel("Packing fraction")
plt.ylabel("Pressure")
plt.ylim([0,10])
plt.plot(pub_data.T[0] * np.pi/6, pub_data.T[1] - 1.0, '-o')
plt.legend(["ZMD","Pressure","published ZMD"])

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
