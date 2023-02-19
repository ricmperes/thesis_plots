import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

import pylars
from pylars.plotting import *


def plot_BV_all_quads():
    all_runs = pd.read_csv('Data/50quads/BV_all.csv',index_col=0)

    fig, ax = plt.subplots(1,1, figsize = (4,3))

    indices = np.where(np.logical_not(np.isnan(all_runs['BV@190K'])))[0]
    med = np.average(all_runs['BV@190K'][indices], 
                     weights=1/all_runs[f'BV@190K_err'][indices]**2)
    wstd = pylars.utils.common.wstd(
        all_runs['BV@190K'][indices], 
        med, 1/all_runs['BV@190K_err'][indices]**2)

    ax.errorbar(all_runs['MPPC#'], all_runs['BV@190K'], 
                yerr= all_runs['BV@190K_err'], 
                ls = '',marker = '.', capsize = 3)

    ax.axhline(med, ls = '--',
               color = plt.rcParams['axes.prop_cycle'].by_key()['color'][1], 
               lw = 2, label = f'Average BV: {med:.2f}$\pm${wstd:.2f}', alpha = 0.5)

    ax.set_ylabel('Breakdown voltage [V]')
    ax.set_xlabel('MPPC #')
    ax.legend()
    ax.set_ylim(46.25,47.75)
    fig.savefig('Figures/allquads_BV.pdf')
    plt.close()

    ##########################

    fig, ax = plt.subplots(1,1, figsize = (3,3))
    
    ax.hist(all_runs['BV@190K'], 
            bins = 20, histtype='step')

    ax.axvline(med, ls = '--',
               color = plt.rcParams['axes.prop_cycle'].by_key()['color'][1], 
               lw = 2, label = f'Average BV: {med:.2f}$\pm${wstd:.2f},',
               alpha = 0.5)

    ax.set_xlabel('Breakdown voltage [V]')
    ax.legend()
    ax.set_xlim(46.25,47.75)
    fig.savefig('Figures/allquads_BV_hist.pdf')
    plt.close()

def plot_BV_all_quads_hybrid():
    all_runs = pd.read_csv('Data/50quads/BV_all.csv',index_col=0)

    fig, axs = plt.subplots(1,2,figsize = (6.5,3), sharey=True,
                            gridspec_kw = {'width_ratios':[0.75,0.25],
                                           'wspace':0}, 
                            tight_layout = True)

    indices = np.where(np.logical_not(np.isnan(all_runs['BV@190K'])))[0]

    med = np.median(all_runs['BV@190K'][indices])#, 
                    # weights=1/all_runs[f'BV@190K_err'][indices]**2)
    wstd = pylars.utils.common.wstd(
        all_runs['BV@190K'][indices], 
        med, 1/all_runs['BV@190K_err'][indices]**2)
    med_err = 1.2533 * wstd/np.sqrt(len(all_runs))

    axs[0].errorbar(all_runs['MPPC#'], all_runs['BV@190K'], 
                yerr= all_runs['BV@190K_err'], 
                ls = '',marker = '.', capsize = 3)

    axs[0].axhline(med, ls = '--',
               color = plt.rcParams['axes.prop_cycle'].by_key()['color'][1], 
               lw = 2, label = f'Median value: ({med:.2f}$\pm${med_err:.2f}) V', 
               alpha = 0.5)

    axs[0].set_ylabel('Breakdown voltage [V]')
    axs[0].set_xlabel('MPPC #')
    axs[0].legend(loc = 'upper left')
    axs[0].set_ylim(46.45,47.6)

    axs[1].hist( all_runs['BV@190K'], bins = 15,
            orientation = 'horizontal', histtype = 'step')
    axs[1].axhline(med, ls = '--',
               color = plt.rcParams['axes.prop_cycle'].by_key()['color'][1], 
               lw = 2, alpha = 0.6)
    axs[1].set_xlabel('MMPC units')
    ax_extra = axs[1].twinx()
    ax_extra.set_yticks(axs[0].get_yticks())
    ax_extra.set_ylim(46.45,47.6)
    ax_extra.set_ylabel('Breakdown voltage [V]')
    #ax_extra.set_yticklabels([t.get_text() for t in axs[1].get_yticklabels()])
    ax_extra.yaxis.set_label_position("right")
    ax_extra.grid(visible=False)

    fig.savefig('Figures/allquads_hybrid_BV.pdf')
    plt.close()

def plot_prop_all_quads(prop, ylabel):
    if prop == 'SPE_res':
        ymin = 2.5
        ymax = 6.5
    elif prop == 'Gain':
        ymin = 2.7e6
        ymax = 3.5e6
    elif prop == 'DCR':
        ymin = 0
        ymax = 9.5
    elif prop == 'CTP':
        ymin = 10
        ymax = 25

    all_runs = pd.read_csv('Data/50quads/properties_52_190.csv',index_col=0)

    fig, ax = plt.subplots(1,1, figsize = (4,3))

    med = np.average(
        all_runs[f'{prop}@190K'], 
        weights=1/all_runs[f'{prop}@190K_err']**2)
    wstd = pylars.utils.common.wstd(
        all_runs[f'{prop}@190K'], med, 
        1/all_runs[f'{prop}@190K_err']**2)
    med_err = 1.2533 * wstd/np.sqrt(len(all_runs))

    if prop == 'CTP':
        ax.plot(all_runs['MPPC#'], all_runs[f'{prop}@190K'], 
                marker = 'o', ls = '')
    else:
        ax.errorbar(all_runs['MPPC#'], all_runs[f'{prop}@190K'], 
                    yerr= all_runs[f'{prop}@190K_err'], 
                    ls = '',marker = '.', capsize = 4)

    ax.axhline(med, ls = '--',
               color = plt.rcParams['axes.prop_cycle'].by_key()['color'][1], 
               lw = 2, 
               label = f'Average: {med:.2f}$\pm${wstd:.2f}', 
               alpha = 0.5)

    ax.set_ylabel(ylabel)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('MPPC #')
    ax.legend()
    fig.savefig(f'Figures/allquads_{prop}.pdf')
    plt.close()

    fig, ax = plt.subplots(1,1, figsize = (3,3))
    
    ax.hist(all_runs[f'{prop}@190K'], 
            bins = 20, histtype='step')

    ax.axvline(med, ls = '--',
               color = plt.rcParams['axes.prop_cycle'].by_key()['color'][1], 
               lw = 2, 
               label = f'Median value: ({med:.2f}$\pm${med_err:.2f}) V ', 
               alpha = 0.5)

    ax.set_xlabel(ylabel)
    ax.set_xlim(ymin, ymax)
    ax.legend(pos='upper left')
    fig.savefig(f'Figures/allquads_{prop}_hist.pdf')
    plt.close()

def plot_prop_all_quads_hybrid(prop, ylabel):


    all_runs = pd.read_csv('Data/50quads/properties_52_190.csv',index_col=0)

    fig, axs = plt.subplots(1,2,figsize = (6.5,3), sharey=True,
                            gridspec_kw = {'width_ratios':[0.75,0.25],
                                           'wspace':0}, 
                            tight_layout = True)

    indices = np.where(np.logical_not(np.isnan(all_runs[f'{prop}@190K'])))[0]
    med = np.median(
        all_runs[f'{prop}@190K'][indices])#, 
        #weights=1/all_runs[f'{prop}@190K_err']**2)
    
    wstd = pylars.utils.common.wstd(
        all_runs[f'{prop}@190K'][indices], med, 
        1/all_runs[f'{prop}@190K_err'][indices]**2)

    med_err = 1.2533 * wstd/np.sqrt(len(all_runs))


    if prop == 'SPE_res':
        ymin = 2.5
        ymax = 6.5
        line_label = f'Median value: ({med:.2f}$\pm${med_err:.2f}) %'
    elif prop == 'Gain':
        ymin = 2.7e6
        ymax = 3.5e6
        line_label = f'Median value: {med:.2e}$\pm${med_err:.2e}'
    elif prop == 'DCR':
        ymin = 0
        ymax = 9.5
        line_label = f'Median value: ({med:.2f}$\pm${med_err:.2f}) Hz/mm$^2$'
    elif prop == 'CTP':
        ymin = 8
        ymax = 25
        line_label = f'Median value: ({med:.2f}$\pm${med_err:.2f}) %'

    axs[0].errorbar(all_runs['MPPC#'], all_runs[f'{prop}@190K'], 
                yerr= all_runs[f'{prop}@190K_err'], 
                ls = '',marker = '.', capsize = 3)

    axs[0].axhline(med, ls = '--',
               color = plt.rcParams['axes.prop_cycle'].by_key()['color'][1], 
               lw = 2, 
               label = line_label, 
               alpha = 0.6)

    axs[0].set_ylabel(ylabel)
    axs[0].set_ylim(ymin, ymax)
    axs[0].set_xlabel('MPPC ID')
    axs[0].legend(loc = 'upper left')

    axs[1].hist(all_runs[f'{prop}@190K'], bins = 15,
            orientation = 'horizontal', histtype = 'step')
    axs[1].axhline(med, ls = '--',
               color = plt.rcParams['axes.prop_cycle'].by_key()['color'][1], 
               lw = 2, alpha = 0.6)
    axs[1].set_xlabel('MMPC units')
    ax_extra = axs[1].twinx()
    ax_extra.set_yticks(axs[0].get_yticks())
    ax_extra.set_ylim(ymin, ymax)
    ax_extra.set_ylabel(ylabel)
    #ax_extra.set_yticklabels([t.get_text() for t in axs[1].get_yticklabels()])
    ax_extra.yaxis.set_label_position("right")
    ax_extra.grid(visible=False)
    fig.savefig(f'Figures/allquads_hybrid_{prop}.pdf')
    plt.close()
