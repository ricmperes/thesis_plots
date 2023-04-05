import matplotlib.pyplot as plt
from astropy import units as u
from snewpy.models.ccsn import Bollig_2016
from snewpy.neutrino import Flavor

def plot_luminosity_curve():
    """Luminosity and mean energy curve in 6 pannels, separated by SN
    phase (burst, accretion, cooling). Uses the Bollig 2016 model with
    LS220-s27.0c EOS (27 Mo).
    """
    
    m27 = Bollig_2016(progenitor_mass=27*u.solMass)
    
    fig, axs = plt.subplots(2,3,figsize = (7,3.5), 
                            gridspec_kw = {'hspace':0.05})
    axs = axs.flatten()
    for ax_i in range(3):
        axs[ax_i].plot(
            m27.time, 
            m27.luminosity[Flavor.NU_E], 
            label=Flavor.NU_E.to_tex(),
            color = 'C0')
        axs[ax_i].plot(
            m27.time, 
            m27.luminosity[Flavor.NU_E_BAR], 
            label=Flavor.NU_E_BAR.to_tex(),
            color = 'C1')
        axs[ax_i].plot(
            m27.time, 
            (m27.luminosity[Flavor.NU_X] + m27.luminosity[Flavor.NU_X_BAR]), 
            label=f'{Flavor.NU_X.to_tex()} + {Flavor.NU_X_BAR.to_tex()}',
            color = 'C2')
        axs[ax_i].plot(
            m27.time, 
            (m27.luminosity[Flavor.NU_X] + 
            m27.luminosity[Flavor.NU_X_BAR] + 
            m27.luminosity[Flavor.NU_E] + 
            m27.luminosity[Flavor.NU_E_BAR]), 
            label=f'Total',
            color = 'C3')
    for ax_i in range(3,6):
        axs[ax_i].plot(
            m27.time, 
            m27.meanE[Flavor.NU_E],
            label=Flavor.NU_E.to_tex(),
            color = 'C0')
        axs[ax_i].plot(
            m27.time, 
            m27.meanE[Flavor.NU_E_BAR], 
            label=Flavor.NU_E_BAR.to_tex(),
            color = 'C1')
        axs[ax_i].plot(
            m27.time, 
            m27.meanE[Flavor.NU_X],
            label=f'{Flavor.NU_X.to_tex()}, {Flavor.NU_X_BAR.to_tex()}',
            color = 'C2')

    axs[0].set_xticklabels([])
    axs[1].set_xticklabels([])
    axs[2].set_xticklabels([])
    for i in range(6):
        axs[i].minorticks_on()
        
    axs[3].set_xlabel('t$_{pb}$ [s]')
    axs[4].set_xlabel('t$_{pb}$ [s]')
    axs[5].set_xlabel('t$_{pb}$ [s]')

    axs[0].set_ylabel('Luminosity [erg/s]')
    axs[3].set_ylabel('<E> [MeV]')

    axs[0].set_xlim(0,0.05)
    axs[0].set_ylim(0,400*1e51)
    axs[1].set_xlim(0.05,1)
    axs[1].set_ylim(0,120*1e51)
    axs[2].set_xlim(1,8)
    axs[2].set_ylim(0,25*1e51)

    axs[3].set_xlim(0,0.05)
    axs[3].set_ylim(2.5,20)
    axs[4].set_xlim(0.05,1)
    axs[4].set_ylim(2.5,20)
    axs[5].set_xlim(1,8)
    axs[5].set_ylim(2.5,20)

    axs[2].legend()
    
    fig.savefig('Figures/luminosity_27Mo.pdf')


if __name__ == '__main__':
    plot_luminosity_curve()