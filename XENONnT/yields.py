"""This file uses code from adapted from 
https://github.com/NESTCollaboration/nestpy/blob/master/tutorials/arxiv/nestpy_tutorial.ipynb"""

import numpy as np
import matplotlib.pyplot as plt
import nestpy

def yields_curve(interaction=nestpy.nr, fields=[81.], 
                 energy_min=1e-1, energy_max=1e2):
    """
    Get yields from nestpy from energy min to energy max 
    """
    energies = np.logspace(np.log10(energy_min), np.log10(energy_max), 1000,)
    energies = np.reshape(energies, (1000,1))
    energies = np.broadcast_to(energies, (len(energies), len(fields)))

    kwargs = {'interaction': interaction,
              'energy': energies, 
              'drift_field': fields}

    ly = nestpy.PhotonYield(**kwargs)/energies
    qy = nestpy.ElectronYield(**kwargs)/energies
    return (energies, ly, qy)

def yields_plot(fields = [200],
                energy_min=0.3, energy_max=150.,
               ):
    '''
    Makes a plot of all the different yields at various energies and field values.
    '''
    
    energies, ly_nr, qy_nr = yields_curve(interaction=nestpy.nr, 
                                    fields=fields, 
                                    energy_min=energy_min, energy_max=energy_max)
    energies, ly_gamma, qy_gamma = yields_curve(interaction=nestpy.gammaRay, 
                                    fields=fields, 
                                    energy_min=energy_min, energy_max=energy_max)
    
    fig, ax = plt.subplots(1,1,figsize = (6,3))
    
    for f, field in enumerate(fields):
        ax.plot(energies[:,f], ly_nr[:,f], 
                 color = 'C0',
               ls = '--')
        ax.plot(energies[:,f], qy_nr[:,f], 
                 color = 'C1',
               ls = '--')
        
        ax.plot(energies[:,f], ly_gamma[:,f], 
                label='Light yield [n$_{ph}$/keV]', color = 'C0',
               ls = '-')
        ax.plot(energies[:,f], qy_gamma[:,f], 
                label='Charge yield [n$_{e}$/keV]', color = 'C1',
               ls = '-')
    
    ax.set_xscale('log')
    ax.set_xlabel('Interaction Energy [keV]')
    ax.set_ylabel('Yield [quanta/KeV]')
    ax.set_xlim(0.3,150)
    ax.legend()
    fig.savefig('Figures/yieds.pdf')

if __name__ == '__main__':
    yields_plot()