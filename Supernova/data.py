import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

#def plot_area_width(): # For some reason not working properly! 
# Axis are stretched
#    hist2d_data = np.load('Data/data_hist2d.npy', allow_pickle=True)
#    hist2d_sn = np.load('Data/sn_hist2d.npy', allow_pickle=True)
#
#    points_data = np.ma.masked_where(hist2d_data[0] == 0, hist2d_data[0])
#    points_sn = np.ma.masked_where(hist2d_sn[0] == 0, hist2d_sn[0])
#
#    fig, ax = plt.subplots(1,1,figsize = (4,2.7))
#
#    ax.pcolormesh(hist2d_data[1],hist2d_data[2],points_data, alpha = 0.4, 
#                  cmap = summer)
#    ax.pcolormesh(hist2d_sn[1],hist2d_sn[2],points_sn, alpha = 1, 
#                  cmap = coolwarm)
#    ax.set_yscale('log')
#    ax.set_xscale('log')
#    ax.set_xlabel('S2 area [pe]')
#    ax.set_ylabel('S2 width [ns]')
#
#    fig.savefig('Figures/sn_area_width.png')
    
def plot_sign_bkg_rates():
    no_cuts = np.loadtxt(
        '/home/atp/rperes/notebooks/thesis_plots/Supernova/Data/rate_bkg_no_cuts.csv', 
        delimiter=',')
    with_cuts = np.loadtxt(
        '/home/atp/rperes/notebooks/thesis_plots/Supernova/Data/rate_bkg_with_cuts.csv', 
        delimiter=',')
    
    no_cuts_x = no_cuts[:,0]
    no_cuts_upper = no_cuts[:,1]
    no_cuts_low = no_cuts[:,2]
    no_cuts_middle = (no_cuts_upper + no_cuts_low)/2
    no_cuts_err = np.abs(no_cuts_upper - no_cuts_middle)

    no_cuts_med = np.median(no_cuts_middle)
    no_cuts_std = np.std(no_cuts_middle)

    with_cuts_x = with_cuts[:,0]
    with_cuts_upper = with_cuts[:,1]
    with_cuts_low = with_cuts[:,2]
    with_cuts_middle = (with_cuts_upper + with_cuts_low)/2
    with_cuts_err = np.abs(with_cuts_upper - with_cuts_middle)

    with_cuts_med = np.median(with_cuts_middle)
    with_cuts_std = np.std(with_cuts_middle)

    SN_rate = 126/7
    SN_rate_std = 5.29/7

    fig, ax = plt.subplots(1,1,figsize = (6,3.5))
    ax.errorbar(no_cuts_x, no_cuts_middle, yerr = no_cuts_err, 
                capsize = 4, ls = '', marker = '.', color = 'C0', label = 'Bkg, no cuts')
    ax.errorbar(with_cuts_x, with_cuts_middle, yerr = with_cuts_err, 
                capsize = 4, ls = '', marker = '.', color = 'C1', label = 'Bkg, with cuts')

    print(no_cuts_med)
    ax.axhline(no_cuts_med, ls = '--', color = 'C0')
    ax.fill_between(np.linspace(0,500,2), no_cuts_med-no_cuts_std, 
                    no_cuts_med+no_cuts_std, alpha = 0.2, color = 'C0')
    print(with_cuts_med)
    ax.axhline(with_cuts_med, ls = '--', color = 'C1')
    ax.fill_between(np.linspace(0,500,2), with_cuts_med-with_cuts_std, 
                    with_cuts_med+with_cuts_std, alpha = 0.2, color = 'C1')
    print(SN_rate)
    ax.axhline(SN_rate, ls = '-.', color = 'C2', label = 'Expected signal rate')
    ax.fill_between(np.linspace(0,500,2), SN_rate-SN_rate_std, 
                    SN_rate+SN_rate_std, alpha = 0.2, color = 'C2')

    ax.set_xlim(0,500)
    ax.set_ylim(0.3,500)
    ax.set_yscale('log')
    ax.set_xlabel('Time since beginning of run [s]')
    ax.set_ylabel('Rate in 7s window [Hz]')
    ax.legend(bbox_to_anchor = (0.645,0.58))
    
    fig.savefig('Figures/signal_bkg_rates.pdf')