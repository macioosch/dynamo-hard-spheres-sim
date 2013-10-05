#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function

from glob import glob
from matplotlib import pyplot as plt
import numpy as np

input_files = glob("csv/convergence-*.csv")

plotted_parameter = "msds_diffusion"
#plotted_parameter = "pressures_collision"
#plotted_parameter = "pressures_virial"

#plotted_parameter = "msds_val"
#plotted_parameter = "times"

legend_names = []

for file_number, file_name in enumerate(sorted(input_files)):
    data = np.genfromtxt(file_name, delimiter='\t', names=[
        "packings","densities","collisions","n_atoms","pressures_virial",
        "pressures_collision","msds_val","msds_diffusion","times",
        "std_pressures_virial","std_pressures_collision","std_msds_val",
        "std_msds_diffusion","std_times"])

    """
    plt.errorbar(data["collisions"],
            np.array(data["pressures_collision"]) * data["densities"][0],
            yerr=np.array(data["std_pressures_collision"]) * data["densities"][0])
    """
    """
    ax = plt.subplot(3, 2, file_number+1)
    plt.errorbar(data["collisions"], data[plotted_parameter],
            yerr=data["std_" + plotted_parameter])
    plt.title("Density {}:".format(data["densities"][0]))
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.4f'))
    """
    plt.errorbar(data["collisions"],
            np.array(data[plotted_parameter]) / data[plotted_parameter][-1] - 1,
            yerr=np.array(data["std_" + plotted_parameter]) \
                    / data[plotted_parameter][-1])
    legend_names.append(data["densities"][0])

plt.legend(legend_names, title="Density:")
plt.show()
