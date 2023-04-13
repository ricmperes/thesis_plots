import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from multimessenger.supernova.Nucleus import Target
from multimessenger.supernova.Xenon_Atom import ATOM_TABLE
from matplotlib.colors import ListedColormap
from matplotlib.colors import ListedColormap, LogNorm
import pandas as pd

# Get the colormap colors, multiply them with the factor "a", and create new colormap
a = 0.85
coolwarm = plt.cm.coolwarm(np.arange(plt.cm.coolwarm.N))
coolwarm[:,0:3] *= a 
coolwarm = ListedColormap(coolwarm)

summer = plt.cm.summer(np.arange(plt.cm.summer.N))
summer[:,0:3] *= a 
summer = ListedColormap(summer)

def plot_s2rate():
    spectrums = pd.read_hdf('Data/area_spectrums.h5')

    fig, ax = plt.subplots(1,1,figsize = (4,2.7))

    ax.step(spectrums['area'],spectrums['bkg_rate'], 
            where = 'mid', label = 'Backgrond rate')
    ax.step(spectrums['area'],spectrums['sn_rate'], 
            where = 'mid', label = 'SN signal rate')
    ax.legend()
    ax.set_xlabel('S2 area [pe]')
    ax.set_ylabel('Diff. rate [Hz/pe]')

    fig.savefig('Figures/s2_rate.pdf')

def plot_area_width():
    hist2d_data = np.load('Data/data_hist2d.npy', allow_pickle=True)
    hist2d_sn = np.load('Data/sn_hist2d.npy', allow_pickle=True)

    points_data = np.ma.masked_where(hist2d_data[0] == 0, hist2d_data[0])
    points_sn = np.ma.masked_where(hist2d_sn[0] == 0, hist2d_sn[0])

    fig, ax = plt.subplots(1,1,figsize = (4,2.7))

    ax.pcolormesh(hist2d_data[1],hist2d_data[2],points_data, alpha = 0.4, 
                  cmap = summer)
    ax.pcolormesh(hist2d_sn[1],hist2d_sn[2],points_sn, alpha = 1, 
                  cmap = coolwarm)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlabel('S2 area [pe]')
    ax.set_ylabel('S2 width [ns]')

    fig.savefig('Figures/sn_area_width.png')
    