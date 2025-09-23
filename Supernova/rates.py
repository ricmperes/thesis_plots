from xenonnt_plot_style import XENONPlotStyle as xps
xps.use('xenonnt')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LogNorm
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FixedLocator

#plt.style.use('../thesis_style.mplstyle')

import nestpy
from scipy.interpolate import interp1d as itp

# Get the colormap colors, multiply them with the factor "a", and create new colormap
a = 0.85
coolwarm = plt.cm.coolwarm(np.arange(plt.cm.coolwarm.N))
coolwarm[:,0:3] *= a 
coolwarm = ListedColormap(coolwarm)


def charge_yield(): #ne/keV
    nc = nestpy.NESTcalc(nestpy.VDetector())
    int = nestpy.INTERACTION_TYPE(0)
    
    _Ers = np.linspace(0,30, 1000)
    _Qc = np.array([nc.GetYields(
        int, _e, drift_field = 23).ElectronYield for _e in _Ers])
    charge_yield_func = itp(_Qc, _Ers)
    
    return charge_yield_func

def plot_charge_yield():
    charge_yield_func = charge_yield()
    
    fig, ax = plt.subplots(figsize = (4,2.7))
    _Ne = np.linspace(0,80,1000)
    ax.plot(_Ne, charge_yield_func(_Ne))
    ax.set_xlim(0,100)
    ax.set_ylim(0,20)
    ax.set_ylabel('E$_R$ [keV]')
    ax.set_xlabel('Electron yield [Ne]')
    
    fig.savefig('Figures/charge_yield.png')

def plot_rates_energy():
    diff_rate_energy = pd.read_csv('Data/diff_rate_energy.csv')
    fig, ax = plt.subplots(figsize = (4,2.7))

    ax.plot(diff_rate_energy.Er, diff_rate_energy.Total, 
            label = 'Total')
    ax.plot(diff_rate_energy.Er, diff_rate_energy.NU_E, 
            label = '$\\nu_e$')
    ax.plot(diff_rate_energy.Er, diff_rate_energy.NU_E_BAR, 
            label = '$\\overline{\\nu}_e$')
    ax.plot(diff_rate_energy.Er, diff_rate_energy['NU_X+NU_X_BAR'], 
            label = '$\\nu_x + \\overline{\\nu}_x$')

    ax.legend(ncols = 1, loc='upper right',
              bbox_to_anchor=(1,0.95))
    ax.set_yscale('log')
    ax.set_xlim(0,20)
    ax.set_ylim(1e-3,16)
    ax.set_ylabel('Diff. rate [keV$^{-1}\cdot$t$^{-1}$]')
    ax.set_xlabel('E$_R$ [keV]')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax2 = ax.twiny()
    
    electron_yield = charge_yield()
    _ne = [0, 20, 40, 60, 80]
    _ne_minor = np.arange(5,95, 5)
    ax2.set_xlim(0,20)
    ax2.plot(np.linspace(0,20,2), (200, 200))
    _e_calc = electron_yield(_ne)
    _e_calc[0] = 0
    ax2.set_xticks(_e_calc,_ne)
    ax2.xaxis.set_minor_locator(FixedLocator(electron_yield(_ne_minor)))
    ax2.set_xlabel("N$_{e^-}$")
    ax.grid(False)
    ax2.grid(False)

    fig.savefig('Figures/diff_rate_energy_n_electrons_XENONstyle.png')

def plot_rates_time():
    diff_rate_time = pd.read_csv('Data/diff_rate_time.csv')
    fig, ax = plt.subplots(figsize = (4,2.7))

    ax.plot(diff_rate_time.time, diff_rate_time.Total, 
            label = 'Total')
    ax.plot(diff_rate_time.time, diff_rate_time.NU_E, 
            label = '$\\nu_e$')
    ax.plot(diff_rate_time.time, diff_rate_time.NU_E_BAR, 
            label = '$\\overline{\\nu}_e$')
    ax.plot(diff_rate_time.time, diff_rate_time['NU_X+NU_X_BAR'], 
            label = '$\\nu_x + \\overline{\\nu}_x$')

    ax.legend(ncols = 4)
    ax.set_ylabel('Diff. rate [Hz$\cdot$t$^{-1}$]')
    ax.set_xlabel('t [s]')
    ax.set_xscale('log')
    ax.set_xlim(1e-3,10)
    
    fig.savefig('Figures/diff_rate_time_XENONstyle.png')

def plot_mass_dependence():
    def get_mass(d, N):
        return N*d**2/2730.788102680283
    def fmt(x):
        return f'{x:.1f} t'

    _ds = np.linspace(1,200,500)
    _N = np.logspace(0,4,300)
    _xx,_yy = np.meshgrid(_ds, _N)
    _zz = get_mass(_xx, _yy)

    fig, ax = plt.subplots(1,1,figsize = (3*1.6,2*1.6), dpi = 120)

    cb = ax.pcolormesh(_ds, _N, _zz, norm = LogNorm())
    contours = ax.contour(_xx,_yy,_zz, [1, 5.9, 40, 100, 1000], colors = 'k', linestyles = '--')
    manual_locations = [(25, 3e0),(50,10),(90,15),(120,30),(170,200)]

    ax.clabel(contours, contours.levels, inline=True, 
            manual = manual_locations, fmt = fmt, 
            fontsize = 8, use_clabeltext=True)
    
    ax.set_yscale('log')
    ax.set_ylabel('Interactions on target')
    ax.set_xlabel('Distance to SN [kpc]')

    fig.colorbar(cb, label = 'Xe active target mass [t]')
    
    fig.savefig('Figures/mass_nevents_3x2.jpeg', dpi = 200)

if __name__ == '__main__':
    plot_rates_energy()
    plot_rates_time()
    # plot_mass_dependence()
    #plot_charge_yield()