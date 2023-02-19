import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LogNorm
from scipy.optimize import curve_fit
from glob import glob
from tqdm import tqdm

import pylars
from pylars.plotting import *

tile_names = ['A','B','C','D','E','F','G','H','J','K','L','M']

def plot_BV_in_air():
    main_data = 'Data/top_array_in_xenoscope/'
    df = pd.read_csv(main_data + 'BV_data.csv', sep = ';')

    chns = list(range(1,12))+[13]

    bvs = []
    bvs_err = []
    fig, axs = plt.subplots(4,3, figsize = (8,10))
    axs = axs.flatten()
    for i, ch in tqdm(enumerate(chns), total = len(chns)):  
        axs[i].errorbar(df['V_bias'], df[f'ch{ch}_amplitude'], 
                        yerr = df[f'ch{ch}_std'], capsize = 4)
        
        par, cov = curve_fit(pylars.utils.common.func_linear,
                            df[f'ch{ch}_amplitude'],
                            df['V_bias'],
                            )
        err = np.sqrt(np.diag(cov))

        bv = par[1]
        bv_err = err[1]

        bvs.append(bv)
        bvs_err.append(bv_err)
        
        _x = np.linspace(52,57,2)
        axs[i].plot(_x, (_x - par[1])/par[0], 
                    label = f'BV: ({bv:.2f}$\pm${bv_err:.2f}) V')
        axs[i].set_xlim(52,57)
        axs[i].set_ylim(0,None)
        axs[i].legend()
        axs[i].set_xlabel('Bias voltage [V]')
        axs[i].set_ylabel('Pulse amplitude [V]')
        axs[i].set_title(f'Tile {tile_names[i]}')
        
    fig.savefig('Figures/air_data.pdf')
    #fig.savefig('Figures/air_data.jpeg')
    plt.close()

    med = np.average(np.array(bvs), weights=1/np.array(bvs_err)**2)
    wstd = pylars.utils.common.wstd(np.array(bvs), med, 1/np.array(bvs_err)**2)
    med_err = wstd/np.sqrt(len(bvs)-1)
    fig, ax = plt.subplots(1,1,figsize = (4.5,3))

    ax.errorbar(np.arange(12), bvs, bvs_err, ls = '', 
                 marker = 'o', capsize = 4)
    ax.set_xlabel('Tile')
    ax.set_ylabel('Breakdown voltage [V]')
    ax.set_xticks(np.arange(12), 
                  tile_names)
    ax.axhline(med, ls = '--', 
               label = f'Average BV: ({med:.2f}$\pm${med_err:.2f}) V')
    ax.legend()
    fig.savefig('Figures/air_data_BV.pdf')
    #fig.savefig('Figures/air_data_BV.jpeg')
    plt.close()

    with open('air_bv.txt','w') as f:
        f.write(f'BV\tBV_err\n')
        for i in range(len(bvs)):
            f.write(f'{bvs[i]}\t{bvs_err[i]}\n')

def plot_light_levels():
    wf_files = glob('Data/top_array_in_xenoscope/C*.txt')
    files_df = pd.DataFrame(columns = ['channel', 'LED_V', 'path', 'ch_n'])

    for _path in tqdm(wf_files):
        _p = _path.split('/')[-1].split('-')[-1].split('_')
        _ch = _p[0]
        _led = float(_p[1][:4])
        files_df = pd.concat((files_df, 
                              pd.DataFrame({'channel' : [_ch],
                                            'LED_V' : [_led],
                                            'path' : [_path],
                                            'ch_n' : [int(_ch[2:])]
                                            })),
                             ignore_index=True)
    files_df = files_df.sort_values(['ch_n', 'LED_V'], ignore_index=True)

    chns = np.sort(np.unique(files_df['ch_n']))

    fig, axs = plt.subplots(6,2, figsize = (8,12))
    axs = axs.flatten()
    for i, _ch in tqdm(enumerate(chns), total = len(chns)):
        mask = (files_df['ch_n'] == _ch)
        _fs = files_df[mask].reset_index()
        
        for j in range(len(files_df[mask])):
            
            wf = np.genfromtxt(_fs.iloc[j]['path'], 
                               delimiter='\t', skip_header=5)
            if wf.shape == (2502,2):
                axs[i].plot(wf[800:1900,0]/1e-6,wf[800:1900,1], 
                            label = f"{_fs.iloc[j]['LED_V']:.2f} V", 
                            alpha = 0.7)
        axs[i].set_ylim(-0.15,1.7)
        axs[i].set_title(f"Tile {tile_names[i]}")
        axs[i].legend(title = 'LED')
        axs[i].set_ylabel('Amplitude [V]')
        axs[i].set_xlabel('Time from trigger [$\mu$s]')
    fig.tight_layout()
    fig.savefig('Figures/air_data_light_levels.pdf')
    #fig.savefig('Figures/air_data_light_levels.jpeg')
    plt.close()