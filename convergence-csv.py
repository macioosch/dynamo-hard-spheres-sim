#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function

from glob import glob
from math import pi
from pprint import pprint
from sys import stdout
from xml.dom import minidom
import bz2
import csv
import matplotlib.pyplot as plt
import re

# local imports
from my_helper_functions_bare import *

# deterministic parameters:
collisions_tuple = ('Duration','TwoParticleEvents')
n_atoms_tuple = ('ParticleCount','val')
packing_tuple = ('PackingFraction','val')
# random parameters:
diffusion_tuple = ('Species','diffusionCoeff')
msds_tuple = ('Species','val')
pressure_tuple = ('Pressure','Avg')
time_tuple = ('Duration','Time')

equilibration = 219700000

input_files = glob("/home/mc/Dropbox/staż 2013/02-hard-spheres/"
        "results/500000_*_*_00_{}_*.xml.bz2".format(equilibration))

data_files = dict()
for file_name in input_files:
    packing, collisions = re.search(
            "/500000_([0-9\.]+)_[0-9]+_00_[0-9]+_([0-9]+)\.xml\.bz2$",
            file_name).groups()
    collisions = int(collisions)
    if packing not in data_files:
        data_files[packing] = dict()
    if collisions not in data_files[packing]:
        data_files[packing][collisions] = []
    data_files[packing][collisions].append(file_name)

stdout_writer = csv.writer(stdout, delimiter='\t')
stdout.write("### Data format: packings\tdensities\tcollisions\tn_atoms\t"
        "pressures_virial\tpressures_collision\tmsds_val\tmsds_diffusion\ttimes\t"
        "std:pressures_virial\tstd:pressures_collision\tstd:msds_val\t"
        "std:msds_diffusion\tstd:times\n")

for packing, collisions_data in sorted(data_files.iteritems()):
    for collisions, file_names in sorted(data_files[packing].iteritems()):

        diffusion, msds, pressure, time = [], [], [], []
        n_atoms = None

        for file_name in file_names:
            xmldoc = minidom.parse(bz2.BZ2File(file_name))

            if n_atoms is None:
                n_atoms = int(xml_get_float(xmldoc, n_atoms_tuple))

            diffusion.append(xml_get_float(xmldoc, diffusion_tuple))
            msds.append(xml_get_float(xmldoc, msds_tuple))
            pressure.append(xml_get_float(xmldoc, pressure_tuple))
            time.append(xml_get_float(xmldoc, time_tuple))

        pressure_collisions = [
                my_pressure(n_atoms, collisions - equilibration, t)
                for t in time ]
        
        stdout_writer.writerow([
            packing,
            "{:.9f}".format(float(packing)*6.0/pi),
            collisions,
            n_atoms,
            my_mean(pressure),
            my_mean(pressure_collisions),
            my_mean(msds),
            my_mean(diffusion),
            my_mean(time),
            my_means_std(pressure),
            my_means_std(pressure_collisions),
            my_means_std(msds),
            my_means_std(diffusion),
            my_means_std(time)
            ])
