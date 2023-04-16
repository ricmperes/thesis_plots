import argparse

parser = argparse.ArgumentParser(
    description=('Redo Xenoscope plots.')
)
parser.add_argument('-l', '--limits',
                    help='Make limits plot.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-p', '--photon',
                    help='Make form factor and cevns matrix plot.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-a', '--all',
                    help='Make all plots.',
                    nargs='?', const=True,
                    default= False,
                    required=False)



args = parser.parse_args()

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from upper_limits import load_files_SI, make_plot_SI
from photon_absorption import plot_photon_absorption
# Load my style ;)

plt.style.use('/home/atp/rperes/notebooks/thesis_plots/thesis_style.mplstyle')

#the lovely coolwarm colormap :)

from matplotlib.colors import ListedColormap

cm = mpl.colormaps.get_cmap('coolwarm')

# Get the colormap colors, multiply them with the factor "a", 
# and create new colormap
a = 0.85
coolwarm = plt.cm.coolwarm(np.arange(plt.cm.coolwarm.N))
coolwarm[:,0:3] *= a 
coolwarm = ListedColormap(coolwarm)

summer = plt.cm.summer(np.arange(plt.cm.summer.N))
summer[:,0:3] *= a 
summer = ListedColormap(summer)

if __name__ == '__main__':
    if args.all:
        plot_limits = plot_photon = True
    else:
        plot_limits = args.limits
        plot_photon = args.photon
    
    if plot_limits:
        SI_limits = load_files_SI()
        make_plot_SI(SI_limits)
    if plot_photon:
        plot_photon_absorption()