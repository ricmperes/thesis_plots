import pandas as pd
import matplotlib.pyplot as plt

def plot_photon_absorption():
    data = pd.read_csv('Data/photon_absorption_xenon.csv',
                   sep = ' ', 
                   names = ['energy','scat_inc','scat_cohe','photoelec',
                            'pair_prod_nuclear','pair_prod_elect','total',
                            'total_no_coherent'],
                   header = None,
                   skiprows=4,
                   index_col=False
                  )

    fig, ax = plt.subplots(1,1,figsize = (6,3.5))

    ax.plot(data['energy']*1e3, data['total'], label = 'Total')
    ax.plot(data['energy']*1e3, data['photoelec'], label = 'Photoelectric effect')
    ax.plot(data['energy']*1e3, data['scat_cohe'], label = 'Compton scattering')
    ax.plot(data['energy']*1e3, data['pair_prod_nuclear'], 
        label = 'Pair production in nucl. field')
    ax.plot(data['energy']*1e3, data['pair_prod_elect'], 
        label = 'Pair production in electron field')

    ax.set_xlabel('Photon energy [keV]')
    ax.set_ylabel('Absorption coefficient [cm$^2$/g]')
    ax.set_xlim(1,1e5)
    ax.set_ylim(1e-4,1e5)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend()

    fig.savefig('Figures/photon_absorption_xe.pdf')

if __name__ == '__main__':
    plot_photon_absorption()