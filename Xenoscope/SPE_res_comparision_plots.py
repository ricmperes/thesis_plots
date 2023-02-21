import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
from scipy.stats import norm

SPE_res_SiPM = 0.05
SPE_res_PMT = 0.25

def get_pe_distribution(n_pe, n_tries, SPE_res):
    hits = poisson.rvs(n_pe, size = int(n_tries))
    SPE_smear = norm.rvs(loc = 0, scale = hits*SPE_res, size = int(n_tries))
    pe = hits + SPE_smear
    return pe

def calculate_meds(arr):
    return np.median(arr), np.std(arr) 

def plot_pe_distributions(PMT_pe, SiPM_pe, figax = None):
    if figax == None:
        fig, ax = plt.subplots(1,1,figsize = (4.5,3))
    else:
        fig, ax = figax
    med_PMT, std_PMT = calculate_meds(PMT_pe)
    
    med_SiPM, std_SiPM = calculate_meds(SiPM_pe)
    
    
    
    _,_,hpmt = ax.hist(PMT_pe, bins = 1000, histtype = 'step', 
                       label = 'PMT', density = True)
    ax.axvline(med_PMT, label = f'median: {med_PMT:.2f}\nstd: {std_PMT:.2f}', 
               color = hpmt[0].get_edgecolor(), ls = '--')

    _,_,hsipm = ax.hist(SiPM_pe, bins = 1000, histtype = 'step', 
                        label = 'SiPM', density = True)
    ax.axvline(med_SiPM, label = f'median: {med_SiPM:.2f}\nstd: {std_SiPM:.2f}', 
               color = hsipm[0].get_edgecolor(), ls = '--')
    ax.legend()
    
    return ((med_PMT, std_PMT), (med_SiPM, std_SiPM), (fig,ax))


def plot_PMT_SiPM_dif():

    pe_list = np.load('Data/other/pe_list.npy')
    PMT_pes_med = np.load('Data/other/PMT_pes_med.npy')
    PMT_pes_std = np.load('Data/other/PMT_pes_std.npy')
    SiPM_pes_med = np.load('Data/other/SiPM_pes_med.npy')
    SiPM_pes_std = np.load('Data/other/SiPM_pes_std.npy')

    fig, axs = plt.subplots(2,1,figsize = (3,7), gridspec_kw={'hspace':0})

    ax2, ax3 = axs.flatten()

    ax2.plot(pe_list, (pe_list-PMT_pes_med)/pe_list *100, label = 'PMT')
    ax2.plot(pe_list, (pe_list-SiPM_pes_med)/pe_list *100, label = 'SiPM')
    ax2.set_ylabel('(Initial-Median)/Initial PE [%]')
    ax2.set_xscale('log')
    ax2.set_xticks([1,1e1,1e2,1e3])

    ax3.plot(pe_list, PMT_pes_std/pe_list)
    ax3.plot(pe_list, SiPM_pes_std/pe_list)
    ax3.set_ylabel('STD/Initial PEs')
    ax3.set_xscale('log')
    ax3.set_xticks([1,10,100,1000])

    ax2.legend()
    ax3.set_xlabel('Initial number of PEs')

    fig.savefig('Figures/SPE_res_comparison.pdf')

def plot_PMT_SiPM_spectrum(n_pe):
    PMT_pe = get_pe_distribution(n_pe = n_pe, n_tries=1e6, SPE_res=SPE_res_PMT)
    SiPM_pe = get_pe_distribution(n_pe = n_pe, n_tries=1e6, SPE_res=SPE_res_SiPM)
    
    fig, ax = plt.subplots(1,1, figsize = (4.5, 3))
    (_,_, (fig,ax)) = plot_pe_distributions(PMT_pe,SiPM_pe, figax = (fig, ax))
    ax.set_xlabel('Measured PEs')
    ax.set_ylabel('SPE-smeared probability density')
    ax.set_yscale('log')

    fig.savefig(f'Figures/PMT_SiPM_spectrum_{n_pe}pe.pdf')
    plt.close()

def plot_PMT_SiPM_spectrums():

    plot_PMT_SiPM_spectrum(2)
    plot_PMT_SiPM_spectrum(10)
    plot_PMT_SiPM_spectrum(50)