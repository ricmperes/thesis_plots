import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.interpolate as itp
from matplotlib.patches import Rectangle

from luminosity_plot import plot_luminosity_curve

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
    print('SNe: making plots go BAAM!')
    plot_luminosity_curve()