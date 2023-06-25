import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LogNorm


# Get the colormap colors, multiply them with the factor "a", and create new colormap
a = 0.85
coolwarm = plt.cm.coolwarm(np.arange(plt.cm.coolwarm.N))
coolwarm[:,0:3] *= a 
coolwarm = ListedColormap(coolwarm)

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

    ax.legend()
    ax.set_yscale('log')
    ax.set_xlim(0,20)
    ax.set_ylim(1e-3,16)
    ax.set_ylabel('Diff. rate [keV$^{-1}\cdot$t$^{-1}$]')
    ax.set_xlabel('E$_R$ [keV]')
    
    fig.savefig('Figures/diff_rate_energy.pdf')

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

    ax.legend()
    ax.set_ylabel('Diff. rate [Hz$\cdot$t$^{-1}$]')
    ax.set_xlabel('t [s]')
    ax.set_xscale('log')
    ax.set_xlim(1e-3,10)
    
    fig.savefig('Figures/diff_rate_time.pdf')

def plot_mass_dependence():
    def get_mass(d, N):
        return N*d**2/2730.788102680283
    def fmt(x):
        return f'{x:.1f} t'

    _ds = np.linspace(1,200,500)
    _N = np.logspace(0,4,300)
    _xx,_yy = np.meshgrid(_ds, _N)
    _zz = get_mass(_xx, _yy)

    fig, ax = plt.subplots(1,1,figsize = (6,3.5))

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
    
    fig.savefig('Figures/mass_nevents.png')

if __name__ == '__main__':
    plot_rates_energy()
    plot_rates_time()
    plot_mass_dependence()