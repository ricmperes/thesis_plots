import numpy as np
import matplotlib.pyplot as plt

def load_files_SI():
    print('Loading csv files for SI WIMP-nucleon cross section!')

    xenon1t_SI = np.loadtxt("Data/limits/xenon1t_SI.csv",delimiter=",")
    cdms = np.loadtxt("Data/limits/CDMSLite2018_SI.csv",delimiter=",")
    cresst = np.loadtxt("Data/limits/CRESSTII_SI_2016_v2.csv",delimiter=",")
    damic = np.loadtxt("Data/limits/DAMIC_2020.csv",delimiter=",")
    darkside = np.loadtxt("Data/limits/darkside50_ul.csv",delimiter=",")
    darwin = np.loadtxt("Data/limits/darwin_SI.csv",delimiter=",")
    deap = np.loadtxt("Data/limits/Deap_SI_2018.csv",delimiter=",")
    lux = np.loadtxt("Data/limits/lux_SI.csv",delimiter=",")
    lz = np.loadtxt("Data/limits/LZ_SI.csv",delimiter=",")
    neutrino = np.loadtxt("Data/limits/neutrino_fog_SI.csv",delimiter=",")
    pandax = np.loadtxt("Data/limits/pandax4t_SI.csv",delimiter=",")
    xenonnt = np.loadtxt("Data/limits/xenonnt_SI.csv",delimiter=",")
    xenon1t_2fold = np.loadtxt("Data/limits/xenon1t_2fold_SI.csv",delimiter=",")
    xenon1t_s2only = np.loadtxt("Data/limits/xenon1t_s2only_SI.csv",delimiter=",")
    
    limits_LXe = {'XENONnT' : xenonnt,
                  'LZ' : lz,
                  'PandaX-4T' : pandax,
                  'XENON1T (2-fold)' : xenon1t_2fold,
                  'XENON1T (S2-only)' : xenon1t_s2only,
                  'DARWIN (projection)' : darwin}
    limits_Ar = {'DEAP' : deap,
                 'Darkside50' : darkside}
    limits_other = {'DAMIC' : damic,
                    'CDMS' : cdms,
                    'CRESST' : cresst}
    limits_neutrino = {'Neutrino fog' : neutrino}

    return limits_LXe,limits_Ar,limits_other,limits_neutrino


def make_plot_SI(limits):
    print('Making SI limits plot.')
    limits_LXe,limits_Ar,limits_other,limits_neutrino = limits

    fig, ax = plt.subplots(1,1,figsize = (6,3))

    for limit_key in limits_LXe.keys():
        ax.plot(limits_LXe[limit_key][:,0],limits_LXe[limit_key][:,1], 
                ls = '-', label = limit_key)
    for limit_key in limits_Ar.keys():
        ax.plot(limits_Ar[limit_key][:,0],limits_Ar[limit_key][:,1],
                ls = '--', label = limit_key)
    for limit_key in limits_other.keys():
        ax.plot(limits_other[limit_key][:,0],limits_other[limit_key][:,1],
                ls = '-.', label = limit_key)
    for limit_key in limits_neutrino.keys():
        ax.fill_between(limits_neutrino[limit_key][:,0],
                        0,
                        limits_neutrino[limit_key][:,1],
                        ls = ':', label = limit_key, 
                        alpha = 0.3,
                        color = 'C6')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e0,1e3)
    ax.set_ylim(1e-50,5e-37)

    ax.set_xlabel('WIMP Mass [GeV/c$^2$]')
    ax.set_ylabel('SI WIMP-nucleon cross section [cm$^2$]')
    ax.legend(loc = 'center left', bbox_to_anchor=(1., 0.5))
    #fig.set_tight_layout(True)
    fig.savefig('Figures/limits_SI.pdf')

if __name__ == '__main__':

    limits = load_files_SI()
    make_plot_SI(limits)