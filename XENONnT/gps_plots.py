import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_gps_effect():
    df_gps = pd.read_csv('Data/gps_corr.csv')
    gps_vlines = np.loadtxt('Data/gps_vlines.csv')
    daq_vlines = np.loadtxt('Data/daq_vlines.csv')

    fig, ax = plt.subplots(1,1,figsize = (4.5,4))

    ax.step(df_gps['t_gps'], df_gps['rate'], c = 'C0', 
            label = 'Binned event rate - GPS time', alpha = 0.9)
    ax.step(df_gps['t_daq'], df_gps['rate'], c = 'C1', 
            label = 'Binned event rate - DAQ time', alpha = 0.9)
    [ax.axvline(_line, c = 'C0', ls = '--', alpha = 0.7
                ) for _line in gps_vlines]
    [ax.axvline(_line, c = 'C1', ls = '--', alpha = 0.7
                ) for _line in daq_vlines]
    
    ax.set_xlabel('Time since first GPS pulse [s]')
    ax.set_ylabel('# of events/2s')
    ax.set_xlim(1759.8, 1820)
    ax.set_ylim(0,25)
    ax.legend()

    fig.savefig('Figures/gps_effect.pdf')

def plot_gps_schematic():
      
    x0 = 7 #center of triangle event
    w = 1.5 # width
    h = 1.5 # height
    daq_gps_diff = 1.48325359
    gps_sync = (2,12)
    daq_sync = (2+daq_gps_diff, 12+daq_gps_diff)

    fig, ax = plt.subplots(1,1,figsize = (4.5,4))

    [ax.axvline(_line, ymin = 0, ymax = 0.5,ls = '--', lw = 2,c = 'C0'
                ) for _line in gps_sync]
    [ax.axvline(_line,  ymin = 0.5,  ymax = 1, ls = '--', lw = 2,c = 'C1'
                ) for _line in daq_sync]
    ax.axhline(0,c='k',lw = 2)

    ax.fill_between([x0-w/2,x0-1/3], [0,-h], [0,0], color = 'C0', 
                    alpha = 0.5,edgecolor="C0", linewidth=0.0)
    ax.fill_between([x0-1/3,x0+w], [-h,0], [0,0], color = 'C0', 
                    alpha = 0.5,edgecolor="C0", linewidth=0.0)
    ax.plot([x0-w/2,x0-1/3], [0,-h], color = 'C0', )
    ax.plot([x0-1/3,x0+w], [-h,0],color = 'C0', )

    ax.fill_between([x0+daq_gps_diff-w/2,x0+daq_gps_diff-1/3], [0,h], [0,0], 
                    alpha = 0.5, color = 'C1',edgecolor="C1", linewidth=0.0)
    ax.fill_between([x0+daq_gps_diff-1/3,x0+daq_gps_diff+w], [h,0], [0,0], 
                    alpha = 0.5, color = 'C1',edgecolor="C1", linewidth=0.0)
    ax.plot([x0+daq_gps_diff-w/2,x0+daq_gps_diff-1/3], [0,h], color = 'C1')
    ax.plot([x0+daq_gps_diff-1/3,x0+daq_gps_diff+w], [h,0], color = 'C1' )

    ax.set_xlim(0,15)
    ax.set_ylim(-2,2)
    ax.set_yticks([])
    ax.set_xlabel('GPS time [s]')
    ax.text(daq_sync[0]+0.5, 1.8, "DAQ frame", horizontalalignment='left', verticalalignment='center')#, fontsize=20)
    ax.text(gps_sync[0]+0.5, -1.8, "GPS frame", horizontalalignment='left', verticalalignment='center')#
    fig.savefig('Figures/gps_schematic.pdf')

if __name__ == '__main__':
    plt.style.use('../thesis_style.mplstyle')
    plot_gps_effect()
    plot_gps_schematic()