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
parser.add_argument('-wr', '--wrates',
                    help='WIMP rates.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-y', '--yields',
                    help='ER and NR yields.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-b', '--bands',
                    help='ER and NR bands.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-wv', '--wvelocity',
                    help='WIMP velocity distribution.',
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
from wimprates_plots import plot_wimp_SI_rates, plot_WIMP_velocity
from yields import yields_plot
from bands import make_band_plot

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
        plot_wimprates = args.wrates
        plot_yields = args.yields
        plot_bands = args.bands
        plt_wvelocity = args.wvelocity

    if plot_limits:
        SI_limits = load_files_SI()
        make_plot_SI(SI_limits)
    if plot_photon:
        plot_photon_absorption()

    if plot_wimprates:
        plot_wimp_SI_rates()
    
    if plot_yields:
        yields_plot()

    if plot_bands:
        print('Making band plot, 20 V/cm')
        make_band_plot(20)
        print('Making band plot, 200 V/cm')
        make_band_plot(200)

    if plt_wvelocity:
        plot_WIMP_velocity()