import numpy as np
import matplotlib.pyplot as plt

def n_fired_ideal(n_photon, pde):
    return n_photon * pde

def n_fired_real(n_photon, pde, n_pixel):
    return n_pixel * (1 - np.exp(-n_photon * pde / n_pixel))

def n_fired_long_pulse(n_photon, pde, n_pixel, pw, t_recover):
    return n_pixel * (1 - np.exp(-n_photon * pde * t_recover / n_pixel / pw))

def plot_non_linearity():
    N_pixels_6x6 = 13923
    N_pixels_quad = N_pixels_6x6 * 4
    PDE = 0.24

    n_photon = np.logspace(1,5.9,200)#np.log10(1.1*N_pixels_quad),200)

    fig, ax = plt.subplots(1,1,figsize = (5,3))
    ax.plot(n_photon, n_photon, label = 'Ideal MPPC, 100% PDE')
    ax.plot(n_photon, n_fired_ideal(n_photon, PDE), label = 'Ideal MPPC, real PDE')
    ax.plot(n_photon, n_fired_real(n_photon, PDE, N_pixels_quad), label = '12×12 mm$^2$ VUV4')
    ax.plot(n_photon, n_fired_real(n_photon, PDE, N_pixels_6x6), label = '6×6 mm$^2$ VUV4')


    ax.axhline(N_pixels_6x6,color = 'grey', ls = '--')
    ax.axhline(N_pixels_quad,color = 'grey', ls = '--')

    ax.ticklabel_format(style='sci', axis='both', scilimits=(0,0), useMathText=True)


    ax.set_ylim(0,1.1*N_pixels_quad)
    ax.text(300000,N_pixels_quad+800, r'Total pixels in a 12×12 mm$^2$ VUV4')
    ax.text(300000,N_pixels_6x6+800, r'Total pixels in a 6×6 mm$^2$ VUV4')
    ax.set_xlim(0,8e5)
    #plt.xscale('log')
    #plt.yscale('log')
    ax.set_ylabel('Triggered pixels')
    ax.set_xlabel('Incident photons')
    ax.legend(frameon = True, loc = 'center right',edgecolor = 'gray')
    #ax.grid()

    fig.savefig('Figures/SiPM_non-linearity.pdf')
    

if __name__ == '__main__':
    plt.style.use('../thesis_style.mplstyle')
    plot_non_linearity()