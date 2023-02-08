import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

import pylars
from pylars.plotting import *

from properties_plots import *
from waveform_plots import *
from cut_plots import *

# Load my style ;)

plt.style.use('../thesis_style.mplstyle')

#the lovely coolwarm colormap :)

from matplotlib.colors import ListedColormap

cm = plt.cm.get_cmap('coolwarm')

# Get the colormap colors, multiply them with the factor "a", and create new colormap
a = 0.85
coolwarm = plt.cm.coolwarm(np.arange(plt.cm.coolwarm.N))
coolwarm[:,0:3] *= a 
coolwarm = ListedColormap(coolwarm)

if __name__ == '__main__':
    plot_properties = False
    plot_waveforms = False
    plot_cuts = True

    if plot_properties == True:
        print('Plotting properties of sensors')
        ## Quad ##
        df_quad = pd.read_hdf('./Data/quad_characterisation.h5')
        BVs_quad = pylars.analysis.breakdown.compute_BV_DCRds_results(df_quad, plot = False)
        plot_gain_v(df_quad, coolwarm, 48, 56, 'quad_gain_v.pdf')
        plot_bv_temp(BVs_quad, 165, 215, 'quad_bv_temp.pdf')
        plot_parameter_vs_gain(df_quad,'SPE_res', 'SPE resolution [%]', 
                            'linear', coolwarm,
                            'quad_errorbars', errorbars = True)
        plot_parameter_vs_gain(df_quad,'SPE_res', 'SPE resolution [%]', 
                            'linear', coolwarm,
                            'quad_NOerrorbars', errorbars = False)
        plot_parameter_vs_gain(df_quad,'DCR', 'DCR [Hz/mm$^2$]', 
                            'linear', coolwarm,
                            'quad_errorbars', errorbars = True)
        plot_parameter_vs_gain(df_quad,'DCR', 'DCR [Hz/mm$^2$]', 
                            'linear', coolwarm,
                            'quad_NOerrorbars', errorbars = False)
        plot_parameter_vs_gain(df_quad,'CTP', 'CTP [%]', 
                            'linear', coolwarm,
                            'quad_errorbars', errorbars = True)
        plot_parameter_vs_gain(df_quad,'CTP', 'CTP [%]', 
                            'linear', coolwarm,
                            'quad_NOerrorbars', errorbars = False)
        ## Quad ##
        df_tile = pd.read_hdf('./Data/tile_characterisation.h5')
        BVs_tile = pylars.analysis.breakdown.compute_BV_DCRds_results(df_quad, plot = False)
        plot_gain_v(df_tile, coolwarm, 48, 56, 'tile_gain_v.pdf')
        plot_bv_temp(BVs_tile, 165, 215, 'tile_bv_temp.pdf')
        plot_parameter_vs_gain(df_tile,'SPE_res', 'SPE resolution [%]', 
                            'linear', coolwarm,
                            'tile_errorbars', errorbars = True)
        plot_parameter_vs_gain(df_tile,'SPE_res', 'SPE resolution [%]', 
                            'linear', coolwarm,
                            'tile_NOerrorbars', errorbars = False)
        plot_parameter_vs_gain(df_tile,'DCR', 'DCR [Hz/mm$^2$]', 
                            'linear', coolwarm,
                            'tile_errorbars', errorbars = True)
        plot_parameter_vs_gain(df_tile,'DCR', 'DCR [Hz/mm$^2$]', 
                            'linear', coolwarm,
                            'tile_NOerrorbars', errorbars = False)
        plot_parameter_vs_gain(df_tile,'CTP', 'CTP [%]', 
                            'linear', coolwarm,
                            'tile_errorbars', errorbars = True)
        plot_parameter_vs_gain(df_tile,'CTP', 'CTP [%]', 
                            'linear', coolwarm,
                            'tile_NOerrorbars', errorbars = False)

    if plot_waveforms == True:
        print('Making waveforms plot.')

        fig, ax = plt.subplots(1,1,figsize = (6,2))
        fig, ax = plot_wf_PEs(figax = (fig, ax))
        fig.savefig('Figures/waveform_PE.pdf')
        plt.close()

        fig, ax = plt.subplots(1,1,figsize = (6,2))
        fig, ax = plot_wf_LED(figax = (fig, ax))
        fig.savefig('Figures/waveform_LED.pdf')
        plt.close()

        fig, ax = plt.subplots(1,1,figsize = (6,2))
        fig, ax = plot_wf_LED_stacked(figax = (fig, ax))
        fig.savefig('Figures/waveform_LED_stacked.pdf')
        plt.close()

    if plot_cuts == True:
        print('Plotting cut effects.')
        plot_length_cut_line()
        plot_length_cut_effect()
        