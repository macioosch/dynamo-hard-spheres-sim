#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function, unicode_literals

from pprint import pprint
from xml.dom import minidom
import bz2
import csv
import glob
import matplotlib.pyplot as plt
import numpy as np
import re

# local imports
from my_helper_functions import *

diffusion_tuple = ('Species','diffusionCoeff')
pressure_tuple = ('Pressure','Avg')

researched_tuple = diffusion_tuple
#researched_tuple = pressure_tuple

input_files = glob.glob("/home/mc/Dropbox/staż 2013/02-hard-spheres/"
        "results/500000_*_00_0_83333333.xml.bz2")
        #"results/500000_*_00_0_25000000.xml.bz2")

packings = dict()
for file_name in input_files:
    packing = re.search("/500000_([0-9\.]+)_[0-9]+_00_0_[0-9]+\.xml\.bz2$",
            file_name).group(1)
    if packing not in packings:
        packings[packing] = []
    packings[packing].append(file_name)

plt.figure(0)
plt.hold(True)

for packing, file_names in sorted(packings.iteritems()):
    parameter = []
    parameter_std = []
    parameter_means_std = []
    collisions = []

    while True:
        collisions.append(int(re.search(
                "/500000_[0-9\.]+_[0-9]+_00_[0-9]+_([0-9]+)\.xml\.bz2$",
                file_names[0]).group(1)))

        parameter_values = []
        for file_name in file_names:
            xmldoc = minidom.parse(bz2.BZ2File(file_name))
            parameter_values.append(xml_get_float(xmldoc, researched_tuple))
                
        parameter.append(np.mean(parameter_values))
        parameter_std.append(np.std(parameter_values))
        parameter_means_std.append(my_means_std(parameter_values))

        print("Packing {}, collisions processed: {}.".format(packing,
            collisions[-1]))

        # check if there are more files in the series
        more_files = glob.glob("/home/mc/Dropbox/staż 2013/02-hard-spheres/"
                "results/500000_{}_*_00_{}_*.xml.bz2".format(packing,
                    collisions[-1]))

        file_names = [ file_name  for file_name in more_files if abs(int(re.search(
                "/500000_[0-9\.]+_[0-9]+_00_[0-9]+_([0-9]+)\.xml\.bz2$",
                file_name).group(1)) - collisions[-1] - collisions[0]) <= 1 ]

        if len(file_names) == 0:
            break

    plt.errorbar(collisions, parameter, yerr=parameter_means_std)
#    plt.errorbar(collisions, parameter/parameter[-1],
#            yerr=parameter_means_std/parameter[-1])


plt.legend(sorted(packings.keys()), loc="lower right", title=u"Współczynnik pakowania:")
plt.xlabel(u"Kolizje")
plt.ylabel(u"Chwilowy współczynnik samodyfuzji D")

plt.show()
