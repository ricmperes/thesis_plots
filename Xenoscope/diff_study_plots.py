import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xenodiffusionscope

def nest_diff_trans_model(field): #cm2/s
    ans = (37.368 * np.power(field, .093452) * 
           np.exp(-8.1651e-5 * field))
    return ans

def plot_transv_diff_literature():
    data = pd.read_csv('Data/diff_studies/diffT_literature.csv', 
                       sep=';', skipinitialspace =True)

    data['D_err_up'] = np.where(data['D_plus'] > 0, 
                                data['D_plus'] - data['D'], 0)
    data['D_err_down'] = np.where(data['D_minus'] > 0, 
                                  data['D'] - data['D_minus'], 0)

    fig, ax = plt.subplots(1,1,figsize = (4.5,3))

    mask_exo = data['drift_field'] < 600
    ax.errorbar(data[mask_exo]['drift_field'], data[mask_exo]['D'], 
                yerr=(data[mask_exo]['D_err_down'], 
                      data[mask_exo]['D_err_down']),
                label = 'EXO-200', marker = 'o', capsize = 4, 
                ls = '')
    ax.errorbar(data[~mask_exo]['drift_field'], data[~mask_exo]['D'], 
                yerr=(data[~mask_exo]['D_err_down'], 
                      data[~mask_exo]['D_err_down']),
                label = 'Doke & Aprille', marker = 'o', capsize = 4, 
                ls = '')
    
    _fields = np.linspace(5,10000,500)
    _nest_model = nest_diff_trans_model(_fields)
    ax.plot(_fields, _nest_model, marker = '', 
            ls = '-', label = 'NEST v2.3.12')

    ax.set_xlabel('Drift Field [V/cm]')
    ax.set_ylabel('Transverse Diffusion Constant [cm$^2$/s]')
    ax.set_xscale('log')
    ax.set_xlim(5,1e4)
    ax.legend()
    fig.savefig('Figures/D_transverse_literature.pdf')
    


def plot_lamp_pulse():
    lamp = xenodiffusionscope.XeLamp(1)
    fig, ax = plt.subplots(1,1,figsize = (3.5,3))
    _t = np.linspace(0,6,100)
    _pulse = lamp.pulse_lamp(_t)
    ax.plot(_t, _pulse/max(_pulse))
    ax.set_ylabel('Relative intensity')
    ax.set_xlabel('t [$\mu$s]')
    fig.savefig('Figures/lamp_pulse.pdf')

def plot_init_pos():
    lamp = xenodiffusionscope.XeLamp(1)
    population = lamp.emitted_electrons_in_interval(0,6)
    x0,y0,z0 = lamp.init_positions(population)
    fig, ax = plt.subplots(1,1,figsize=(3.5,3))
    hh = ax.hist2d(x0,y0, bins = 200, cmin = 1, cmap = coolwarm)
    ax.set_aspect('equal')
    ax.set_ylim(-3,3)
    ax.set_xlim(-3,3)
    ax.set_xlabel('x [mm]')
    ax.set_ylabel('y [mm]')
    fig.colorbar(hh[3],label= 'Number of initial electrons')
    fig.savefig('Figures/init_positions.png')


if __name__ == '__main__':
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

    summer = plt.cm.summer(np.arange(plt.cm.summer.N))
    summer[:,0:3] *= a 
    summer = ListedColormap(summer)
    
    ### Plots
    #plot_transv_diff_literature()
    plot_lamp_pulse()
    plot_init_pos()
