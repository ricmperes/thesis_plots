import numpy as np
import matplotlib.pyplot as plt

from pylars.plotting import *

def plot_length_cut_line(length_cut = 10, figax = None):
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (3,2.6), dpi = 100)
    else:
        fig, ax = figax

    data = np.load('Data/quad_length_histogram.npy', 
        allow_pickle=True)

    bin_centers = (data[1][1:] + data[1][:-1])/2

    ax.step(bin_centers, data[0], where = 'mid')
    ax.axvline(length_cut, label = f'Length cut: {length_cut}', 
               c = plt.rcParams['axes.prop_cycle'].by_key()['color'][1])

    ax.set_xlabel('Pulse length [# samples]')

    ax.legend()
    
    fig.savefig('Figures/length_cut_histogram.pdf')



def plot_length_cut_effect(figax = None):
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (3,2.6), dpi = 100)
    else:
        fig, ax = figax

    data_no_cuts = np.load('Data/quad_area_histogram_nocuts.npy', 
        allow_pickle=True)
    
    data_length_cuts = np.load('Data/quad_area_histogram_lengthcut.npy', 
        allow_pickle=True)

    bin_centers = (data_no_cuts[1][1:] + data_no_cuts[1][:-1])/2

    ax.step(bin_centers, data_no_cuts[0], where = 'mid',
        label = 'No cuts', alpha = 0.7)
    ax.step(bin_centers, data_length_cuts[0], where = 'mid',
        label = 'Length > 10', alpha = 0.7)

    ax.set_xlabel('Pulse area [integrated ADC counts]')
    ax.set_yscale('log')
    ax.legend()
    
    fig.savefig('Figures/length_cut_effect.pdf')

