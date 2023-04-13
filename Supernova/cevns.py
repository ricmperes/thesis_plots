import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from multimessenger.supernova.Nucleus import Target
from multimessenger.supernova.Xenon_Atom import ATOM_TABLE
from matplotlib.colors import ListedColormap
from matplotlib.colors import ListedColormap, LogNorm


# Get the colormap colors, multiply them with the factor "a", and create new colormap
a = 0.85
coolwarm = plt.cm.coolwarm(np.arange(plt.cm.coolwarm.N))
coolwarm[:,0:3] *= a 
coolwarm = ListedColormap(coolwarm)

def plot_formfactor():
    fig, ax = plt.subplots(1,1,figsize = (4,2.7))
    
    xe_isotopes = ['Xe129','Xe131','Xe132','Xe134','Xe136',]
    for xe in xe_isotopes:
        recoil_en = np.linspace(0,200,100) * u.keV
        singleXe = Target(ATOM_TABLE[xe], pure=True)
        formfac = singleXe.form_factor(recoil_en)

        
        ax.plot(recoil_en, formfac**2, label = ATOM_TABLE[xe]['Type'])
    ax.set_yscale('log')
    ax.set_xlabel('E$_R$ [keV]')
    ax.set_ylabel('$F(q^2)^2$')
    ax.set_xlim(0,200)
    ax.set_ylim(1e-7, 1)
    ax.legend()
    fig.savefig('Figures/form_factor_all_isotopes.pdf')

def plot_cevns_matrix():
    recoil_en = np.linspace(0,50,100) * u.keV
    neutrino_en = np.linspace(0,120, 100)*u.MeV
    singleXe = Target(ATOM_TABLE['Xe131'], pure=True)
    crosssec = singleXe.nN_cross_section(neutrino_en, recoil_en)

    fig, ax = plt.subplots(1,1,figsize = (3.8,2.53))
    matrix = ax.pcolormesh(neutrino_en.value, recoil_en.value, 
                           crosssec.to(u.cm**2/u.keV), norm = 'linear', 
                    vmin = 0, cmap=coolwarm) #, norm=LogNorm())
    fig.colorbar(matrix, label = "$d\sigma/(dE_\\nu \cdot dE_R)$ [cm$^2$/keV/MeV]")
    ax.set_ylabel('$E_R [keV]$')
    ax.set_xlabel('$E_\\nu [MeV]$')
    
    fig.savefig('Figures/cevns_matrix.png')

if __name__ == '__main__':
    plot_formfactor()
    plot_cevns_matrix()



