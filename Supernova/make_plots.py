import argparse

parser = argparse.ArgumentParser(
    description=('Redo Xenoscope plots.')
)
parser.add_argument('-l', '--lightcurve',
                    help='Make lightcurve plot (6 pannels).',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-c', '--cevns',
                    help='Make form factor and cevns matrix plot.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-r', '--rates',
                    help='Make rate vs energy ant time plots.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-s', '--significance',
                    help='Make signficicance curves plot.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-d', '--data',
                    help='Make data compare plots.',
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
import pandas as pd
import scipy.interpolate as itp
from matplotlib.patches import Rectangle

from luminosity_plot import plot_luminosity_curve
from cevns import plot_formfactor, plot_cevns_matrix
from rates import plot_rates_energy, plot_rates_time, plot_mass_dependence
from data import plot_s2rate, plot_sign_bkg_rates
from significance_distance import plot_significances

# Load my style ;)
plt.style.use('/home/atp/rperes/notebooks/thesis_plots/thesis_style.mplstyle')
from matplotlib.colors import ListedColormap

# Get the colormap colors, multiply them with the factor "a", and create new colormap
a = 0.85
coolwarm = plt.cm.coolwarm(np.arange(plt.cm.coolwarm.N))
coolwarm[:,0:3] *= a 
coolwarm = ListedColormap(coolwarm)

if __name__ == '__main__':
    if args.all:
        plot_lightcurve = plot_cevns = plot_rates = plot_significance = plot_data = True
    else:
        plot_lightcurve = args.lightcurve
        plot_cevns = args.cevns
        plot_rates = args.rates
        plot_significance = args.significance
        plot_data = args.data

    if plot_lightcurve:
        print('SNe: making plots go BAAM!')
        plot_luminosity_curve()
    
    if plot_cevns:
        print('Plotting ff and cevns.')
        plot_formfactor()
        plot_cevns_matrix()

    if plot_rates:
        print('Plotting rates over energy and time.')
        plot_rates_energy()
        plot_rates_time()
        plot_mass_dependence()

    if plot_significance:
        print('Plotting significane curves.')
        plot_significances()

    if plot_data:
        print('Plotting data and SN signal.')
        plot_area_width()
        plot_s2rate()
        plot_sign_bkg_rates()
    

