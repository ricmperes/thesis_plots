import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from pylars.plotting import *
from pylars.utils.common import func_linear

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
    fig, ax = plt.subplots(1,1, figsize = (3.5,3.5))

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
    ax.set_ylim(0,6.2e6)
    ax.set_xlim(48,56)
    ax.set_xlabel('Bias voltage [V]')
    ax.set_ylabel('Gain')
    ax.legend()
    fig.savefig('Figures/' + plotname)
    plt.close()
    
def plot_bv_temp(BVs, tmin, tmax, plotname):
    fig, ax = plt.subplots(1,1, figsize = (4,2.5))

    #linres = stats.linregress(BVs['T'], BVs['BV'])
    par, cov = curve_fit(
        func_linear, BVs['T'], BVs['BV'], sigma=1/BVs['BV_error']**2)
    err = np.sqrt(np.diag(cov))

    print(f'a: {par[0]} +- {err[0]}')
    print(f'b: {par[1]} +- {err[1]}')

    _x = np.linspace(tmin,tmax, 2)

    ax.errorbar(BVs['T'], BVs['BV'], yerr=BVs['BV_error'], ls = '')
    ax.plot(_x, func_linear(_x, *par), marker = '', ls = '-')

    ax.set_xlabel('Temperature [K]')
    ax.set_ylabel('Breakdown Voltage [V]')
    ax.set_xlim(tmin, tmax)
    fig.savefig('Figures/' + plotname)
    plt.close()

    
def plot_parameter_vs_gain(df,parameter, ylabel, yscale, cmap,
                           plotlabel, errorbars:bool = True):
    temps = np.unique(df['T'])
    fig, ax = plt.subplots(1,1,figsize = (3.5,3.5))
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
    plt.close()