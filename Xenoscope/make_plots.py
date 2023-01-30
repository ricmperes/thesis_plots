import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

import pylars
from pylars.plotting import *

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

# Fit functions
from scipy.optimize import curve_fit

def DCR_fit_func(x, a, b):
    ans = np.exp(a*x + b)
    return ans

def SPE_fit_func(x, a,b,c):
    ans = np.exp(-a*x+b)+c
    return ans

def CTP_fit_func(x, a,b,c):
    ans = np.exp(a*x+b)+c
    return ans

# 6x6 vs quad vx tile #

def plot_gain_v(df, cmap, xmin, xmax, plotname):
    temps = np.unique(df['T'])
    fig, ax = plt.subplots(1,1, figsize = (5,5))

    _x = np.linspace(xmin,xmax, 100)

    for i, t in enumerate(temps):
        _mask = df['T'] == t
        linres = stats.linregress(df[_mask]['V'], df[_mask]['Gain'])
        ax.plot(_x, linres.slope*_x+linres.intercept, marker ='', ls ='-',
               c = cmap(i/len(temps)))

        ax.errorbar(df[_mask]['V'], 
                df[_mask]['Gain'], yerr= df[_mask]['Gain_error'],
                marker = '.', ls ='',
                label = f'{t:.0f} K',
                    capsize = 3,
               c = cmap(i/len(temps)))

    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
    ax.set_xlabel('Bias voltage [V]')
    ax.set_ylabel('Gain')
    ax.legend()
    fig.savefig('Figures/' + plotname)
    
def plot_bv_temp(BVs, tmin, tmax, plotname):
    fig, ax = plt.subplots(1,1, figsize = (5,3))

    linres = stats.linregress(BVs['T'], BVs['BV'])
    _x = np.linspace(tmin,tmax, 2)

    ax.errorbar(BVs['T'], BVs['BV'], yerr=BVs['BV_error'], ls = '')
    ax.plot(_x, linres.slope * _x + linres.intercept)

    ax.set_xlabel('Temperature [K]')
    ax.set_ylabel('Breakdown Voltage [V]')
    ax.set_xlim(tmin, tmax)
    fig.savefig('Figures/' + plotname)

    
def plot_parameter_vs_gain(df,parameter, ylabel, yscale, cmap,
                           plotlabel, errorbars:bool = True):
    temps = np.unique(df['T'])
    fig, ax = plt.subplots(1,1,figsize = (5,5))
    for i, t in enumerate(temps):
        _mask = df['T'] == t
        
        if errorbars:
            ax.errorbar(df[_mask]['Gain'], 
                        df[_mask][parameter], 
                        yerr = df[_mask][f'{parameter}_error'],
                        marker = '.', ls ='', capsize = 3,
                        label = f'{t:.0f} K',
                        c = cmap(i/len(temps)))
       
        else:
            ax.plot(df[_mask]['Gain'], 
                    df[_mask][parameter], 
                    marker = 'o', ls ='',
                    label = f'{t:.0f} K',
                    c = cmap(i/len(temps)))
        

    ax.ticklabel_format(style='sci', axis='x', 
                            scilimits=(0,0), useMathText=True)
    
    ax.set_yscale(yscale)
    ax.set_xlabel('Gain')
    ax.set_ylabel(ylabel)
    ax.legend()
   
    fig.savefig(f'Figures/{plotlabel}_{parameter}_gain.pdf')

if __name__ == '__main__':
    
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
