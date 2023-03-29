import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d


@np.vectorize
def get_P_Xe(m, xe_p_from_dens, M = 131.293, n_bottles = 1, 
             V = None, Volume_per_bottle = 40):
    n = m*1000/M
    if V is None:
        V = n_bottles * Volume_per_bottle
    dens = n/V
    try:
        P = xe_p_from_dens(dens)
    except:
        P = np.nan
    return P

def make_xe_mass_plot():

    M = 131.293 #g/mol
    Volume_per_bottle = 40 #L

    xe_properties_1 = pd.read_csv(
        'Data/xe_dens_nist/Xe_density_at_300.txt',
        delimiter= '\t')
    xe_properties_2 = pd.read_csv(
        'Data/xe_dens_nist/Xe_density_at_300_high_pressure.txt',
        delimiter= '\t')

    xe_properties = pd.concat([xe_properties_1,xe_properties_2], 
                              ignore_index = True)

    xe_p_from_dens = interp1d(xe_properties['Density (mol/l)'], 
                              xe_properties['Pressure (bar)']) #l/mol

    _m = np.linspace(0,450,200)
    n_bottle = [1, 3, 6, 10]

    fig, ax = plt.subplots(1,1,figsize=(6.5,4))
    for _n_bottles in n_bottle:
        if _n_bottles == 1:
            ax.plot(_m, get_P_Xe(_m, xe_p_from_dens = xe_p_from_dens, 
                                 M = M, n_bottles = _n_bottles, 
                                 V = None, 
                                 Volume_per_bottle = Volume_per_bottle), 
                    label = f'{_n_bottles} bottle')
        else:
            ax.plot(_m, get_P_Xe(_m, xe_p_from_dens = xe_p_from_dens, 
                                 M = M, n_bottles = _n_bottles, 
                                 V = None, 
                                 Volume_per_bottle = Volume_per_bottle), 
                    label = f'{_n_bottles} bottles')
    ax.axhline(200, label = 'Safety limit of bottle (200 bar)', 
               ls = '--', c = 'gray')

    ax.set_xlim(0,450)
    ax.set_xlabel('Mass of Xe inside [kg]')
    ax.set_yscale('log')
    ax.set_ylabel('Pressure at 300 K [bar]')
    ax.legend()
    fig.savefig('Figures/xe_mass_bottles.pdf')

    plt.close()