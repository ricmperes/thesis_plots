import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    

if __name__ == '__main__':
    # Load my style ;)

    plt.style.use('../thesis_style.mplstyle')
    plot_transv_diff_literature()
