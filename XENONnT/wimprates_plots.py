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

def plot_WIMP_velocity():
    from scipy import  stats
    kms = nu.km/nu.s

    from wimprates import StandardHaloModel, v_earth
    v_0, v_esc = StandardHaloModel().v_0, StandardHaloModel().v_esc

    def galactic_v_dist(v):
        # Maxwell Boltzmann distribution with
        # 1/2 m v0**2 = k T <=> v0**2 = 2 k T / m = 2 a**2 <=> a = v_0/sqrt(2)
        # Cut off above escape velocity (and renormalized)
        # See Donato et al, https://arxiv.org/pdf/hep-ph/9803295.pdf, eq. 4/5
        dist = stats.maxwell(scale=v_0/2**0.5)
        y = dist.pdf(v) / dist.cdf(v_esc)
        if isinstance(v, np.ndarray):
            y[v > v_esc] = 0
        elif v > v_esc:
            return 0
        return y

    from wimprates import observed_speed_dist

    vs = np.linspace(0, 810 * kms, 100000)

    fig, ax = plt.subplots(1,1,figsize = (4, 2.5))

    ax.plot(vs / kms, galactic_v_dist(vs) * kms,
            label='Galactic frame')
    ax.plot(vs / kms, observed_speed_dist(vs) * kms,
            label='Local frame')
    ax.axvline(v_0/ kms, ls = '--', alpha = 0.8, 
               color = 'C0')#label = '$v_0$',
    ax.axvline(v_esc/ kms, ls = ':', alpha = 0.8, 
               color = 'C0')#, label = '$v_{esc}$'
    ax.axvline((v_0**2 + v_earth()**2)**0.5 / kms, 
               ls = '--', alpha = 0.8, color = 'C1')#label = '$v_0$',
    ax.axvline((v_esc + v_earth()) / kms, ls = ':', 
               alpha = 0.8, color = 'C1')#, label = '$v_{esc}$'


    ax.set_ylabel("PDF [(km/s)$^{\mathrm{-1}}]$")
    ax.set_xlabel("Speed [km/s]")
    ax.legend()
    ax.set_ylim(0,0.004)
    ax.set_xlim(0,810)

    fig.savefig('Figures/wimp_velocity.pdf')

plt.show()

if __name__ == '__main__':
    plot_wimp_SI_rates()
    plot_WIMP_velocity()