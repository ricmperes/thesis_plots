import numpy as np
import matplotlib.pyplot as plt
import wimprates as wr
import numericalunits as nu


def plot_wimp_SI_rates():
    wimp_masses = [10,100]
    materials = ['Xe', 'Ar', 'Ge', 'Si']
    ers = np.linspace(0,100,500)

    fig, ax = plt.subplots(1,1,figsize = (4,2.5))

    for i, _wimp_mass in enumerate(wimp_masses):
        for j, _mat in enumerate(materials):
            _rates = wr.elastic_nr.rate_elastic(
                erec = ers *nu.keV,
                mw = _wimp_mass *nu.GeV/nu.c0**2,
                sigma_nucleon=1e-47 *nu.cm**2/ (
                    nu.year**-1 * nu.tonne**-1 * nu.keV**-1),
                material = _mat)
            ax.plot(ers, _rates, label = (_mat if i==1 else None), 
                    ls = ('--' if i==0 else '-'), 
                    color = f'C{j}')

    ax.legend()
    ax.set_yscale('log')
    ax.set_xlabel('Recoil energy [keV$_{NR}$]')
    ax.set_ylabel('Rate [t$^{-1}$ y$^{-1}$ keV$^{-1}$]')
    ax.set_ylim(1e-4,0.8)
    ax.set_xlim(0,100)

    fig.savefig('Figures/wimp_rates.pdf')

if __name__ == '__main__':
    plot_wimp_SI_rates()