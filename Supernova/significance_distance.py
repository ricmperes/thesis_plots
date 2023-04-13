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

Xe_dens = 2.8568 #t/m^3
@np.vectorize
def sn_n_events(d,m): #integrated in time
    d_set_sn_point_10kpc = 10
    return 6 * 8 / (np.pi*0.6**2*1.5*Xe_dens) * d_set_sn_point_10kpc**2/d**2 *m

@np.vectorize
def Z0(n,b):
    if n>b:
        return np.sqrt(2*(n*np.log(n/b)+b-n))
    else:
        return 0

def bkg_rate(m: float, scale_by = 'Area'):
    """Calculate bkg rate increased linearly with area for a given mass.

    Args:
        m (float): mass of the target in tonnes of Xe
    """
    
    A_nT = np.pi*0.75**2
    A_new = np.pi * (m/(2*np.pi*Xe_dens))**(2/3)
    V_nT = 2*np.pi*0.75**3
    V_new = m/Xe_dens
    XenT_bkg = 2 *8 #integrated in 8 s, per tonne
    if scale_by == 'Volume':
        return XenT_bkg * V_new/V_nT
    else:
        return XenT_bkg * A_new/A_nT


def plot_significances():
    
    d_list = np.linspace(1, 300, 1000)
    nT = Z0(bkg_rate(5.9,scale_by='Area') + sn_n_events(d_list,5.9),bkg_rate(5.9,scale_by = 'Area'))
    new_20t = Z0(bkg_rate(20,scale_by='Area') + sn_n_events(d_list,20),bkg_rate(20,scale_by = 'Area'))
    new_60t = Z0(bkg_rate(60,scale_by='Area') + sn_n_events(d_list,60),bkg_rate(60,scale_by = 'Area'))
    new_100t = Z0(bkg_rate(100,scale_by='Area') + sn_n_events(d_list,100),bkg_rate(100,scale_by = 'Area'))
    
    #new_20t = Z0(bkg_rate(20,scale_by='Area')/10 + sn_n_events(d_list,20),bkg_rate(20,scale_by = 'Area')/10)
    #new_60t = Z0(bkg_rate(60,scale_by='Area')/10 + sn_n_events(d_list,60),bkg_rate(60,scale_by = 'Area')/10)
    #new_100t = Z0(bkg_rate(100,scale_by='Area')/10 + sn_n_events(d_list,100),bkg_rate(100,scale_by = 'Area')/10)
    
    fig, ax = plt.subplots(1,1,figsize = (6,4))

    ax.plot(d_list, nT, label = 'XENONnT')
    ax.plot(d_list, new_20t, label = 'Next gen - 20 t')
    ax.plot(d_list, new_60t, label = 'Next gen - 60 t')
    ax.plot(d_list, new_100t, label = 'Next gen - 100 t')

    ax.axhline(5, ls = '-.', c='grey')#,label = '5$\sigma$')
    ax.axhline(3, ls = '--', c = 'grey')#,label = '3$\sigma$')
    ax.set_yscale('log')
    ax.minorticks_on()
    ax.set_yticks([1,3,5,10,20],[1,3,5,10,20])
    ax.set_ylim(0.5,20)
    ax.set_xlim(0,180)
    ax.set_xlabel('Distance to SN [kpc]')
    ax.set_ylabel('$\\nu$ signal significance [$\sigma$]')
    ax.legend()
    fig.savefig('Figures/Significance_vs_distance.pdf')
    

if __name__ == '__main__':
    plot_significances()