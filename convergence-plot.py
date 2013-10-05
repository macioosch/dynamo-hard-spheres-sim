#!/usr/bin/env python2
# encoding=utf-8
from __future__ import division, print_function

from glob import glob
from itertools import izip
from matplotlib import pyplot as plt
import numpy as np

input_files = glob("csv/convergence-*.csv")

plotted_parameter = "msds_diffusion"
#plotted_parameter = "pressures_collision"
#plotted_parameter = "pressures_virial"

#plotted_parameter = "msds_val"
#plotted_parameter = "times"

skip_points = 20

legend_names = []

for file_number, file_name in enumerate(sorted(input_files)):
    data = np.genfromtxt(file_name, delimiter='\t', names=[
        "packings","densities","collisions","n_atoms","pressures_virial",
        "pressures_collision","msds_val","msds_diffusion","times",
        "std_pressures_virial","std_pressures_collision","std_msds_val",
        "std_msds_diffusion","std_times"])
    n_atoms = data["n_atoms"][0]
    density = data["densities"][0]
    equilibrated_collisions = data["collisions"] - 2*data["collisions"][0] \
            + data["collisions"][1]

    """
    ###   5 graphs: D(CPS)   ###
    ax = plt.subplot(3, 2, file_number+1)
    plt.errorbar((equilibrated_collisions / n_atoms)[skip_points:],
            data[plotted_parameter][skip_points:],
            yerr=data["std_" + plotted_parameter][skip_points:])
    plt.title("Density {}:".format(data["densities"][0]))
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.4f'))
    plt.xlabel("Collisions per sphere")
    plt.ylabel("D")
    """
    """
    ###   5 graphs: D(1/CPS)   ###
    ax = plt.subplot(3, 2, file_number+1)
    plt.plot((n_atoms / equilibrated_collisions)[skip_points:],
            data[plotted_parameter][skip_points:])
    plt.title("Density {}:".format(data["densities"][0]))
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.4f'))
    plt.xlim(xmin=0)
    plt.xlabel("1 / Collisions per sphere")
    plt.ylabel("D")
    """
    """
    ###   1 graph: D(CPS) / Dinf   ###
    plt.errorbar(equilibrated_collisions / n_atoms,
            data[plotted_parameter] / data[plotted_parameter][-1] - 1,
            yerr=data["std_" + plotted_parameter] / data[plotted_parameter][-1])
    legend_names.append(data["densities"][0])
    plt.xlabel("Collisions per sphere")
    plt.ylabel("D / D(t --> inf)")
    """
    """
    ###   1 graph: D(1/CPS) / Dinf   ###
    plt.plot( n_atoms / equilibrated_collisions,
            data[plotted_parameter] / data[plotted_parameter][-1] - 1)
    legend_names.append(data["densities"][0])
    plt.xlabel(" 1 / Collisions per sphere")
    plt.ylabel(plotted_parameter)
    """

#plt.legend(legend_names, title="Density:", loc="lower right")
#plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)

plt.show()
