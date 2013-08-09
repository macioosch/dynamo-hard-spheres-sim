#!/usr/bin/env python2

from xml.dom import minidom
import glob
import numpy as np
import matplotlib.pyplot as plt

packings = []
pressures = []
msds_val = []
msds_diffusion = []
collisions = []
times = []
N_atoms = []

for file in sorted(glob.glob("config.start.*.output.xml")):
    xmldoc = minidom.parse(file)
    packings.append( float( 
        xmldoc.getElementsByTagName('PackingFraction')[0].attributes['val'].value))
    pressures.append(float(
        xmldoc.getElementsByTagName('Pressure')[0].attributes['Avg'].value))
    msds_val.append(float(
        xmldoc.getElementsByTagName('Species')[0].attributes['val'].value))
    msds_diffusion.append(float(
        xmldoc.getElementsByTagName('Species')[0].attributes['diffusionCoeff'].value))
    collisions.append(float(
        xmldoc.getElementsByTagName('Duration')[0].attributes['TwoParticleEvents'].value))
    times.append(float(
        xmldoc.getElementsByTagName('Duration')[0].attributes['Time'].value))
    N_atoms.append(float(
        xmldoc.getElementsByTagName('ParticleCount')[0].attributes['val'].value))

ZMD = np.sqrt(np.pi)*np.array(collisions) / (3*np.array(N_atoms)*np.array(times))

plt.figure(1)
plt.plot(packings, ZMD, '-o', packings, pressures, '-o')
plt.xlabel("Packing fraction")
plt.ylabel("Pressure")
plt.ylim([0,10])

pub_data = np.genfromtxt('published-values.csv', delimiter=' ')
plt.plot(pub_data.T[0] * np.pi/6, pub_data.T[1] - 1.0, '-o')

plt.legend(["ZMD","Pressure","published ZMD"])

"""
plt.figure(2)
plt.semilogy(packings, msds_val, '-o')
plt.semilogy(packings, msds_diffusion, '-o')
plt.xlabel("Packing fraction")
plt.ylabel("MSD, diffusion coef.")
plt.legend(["MSD","diffusion coef."])
"""

plt.show()
