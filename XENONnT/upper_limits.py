import numpy as np
import matplotlib.pyplot as plt

def load_files_SI():
    print('Loading csv files for SI WIMP-nucleon cross section!')

    xenon1t_SI = np.loadtxt("Data/limits/xenon1t_SI.csv",delimiter=",")
    cdms = np.loadtxt("Data/limits/CDMSLite2018_SI.csv",delimiter=",")
    cresst = np.loadtxt("Data/limits/CRESSTII_SI_2016_v2.csv",delimiter=",")
    damic = np.loadtxt("Data/limits/DAMIC_2020.csv",delimiter=",")
    darkside_low = np.loadtxt("Data/limits/darkside50_lowmass_ul.csv",delimiter=",")
    darwin = np.loadtxt("Data/limits/darwin_SI.csv",delimiter=",")
    deap = np.loadtxt("Data/limits/Deap_SI_2018.csv",delimiter=",")
    lux = np.loadtxt("Data/limits/lux_SI.csv",delimiter=",")
    lz = np.loadtxt("Data/limits/LZ_SI.csv",delimiter=",")
    neutrino = np.loadtxt("Data/limits/neutrino_fog_SI.csv",delimiter=",")
    pandax = np.loadtxt("Data/limits/pandax4t_SI.csv",delimiter=",")
    xenonnt = np.loadtxt("Data/limits/xenonnt_SI.csv",delimiter=",")
    xenon1t_2fold = np.loadtxt("Data/limits/xenon1t_2fold_SI.csv",delimiter=",")
    xenon1t_s2only = np.loadtxt("Data/limits/xenon1t_s2only_SI.csv",delimiter=",")
    supercdms = np.loadtxt("Data/limits/SuperCDMS_SI.csv",delimiter=",")
    darkside_high = np.loadtxt("Data/limits/DS-50.csv",delimiter=",")

    limits = {'XENONnT' : xenonnt,
              'LZ' : lz,
              'PandaX-4T' : pandax,
              'XENON1T (2-fold)' : xenon1t_2fold,
              'XENON1T (S2-only)' : xenon1t_s2only,
              'DARWIN (projection)' : darwin,
              'DEAP-3600' : deap,
              'Darkside-50_low' : darkside_low,
              'Darkside-50_high' : darkside_high,
              'DAMIC' : damic,
              'CDMSLite' : cdms,
              'SuperCDMS' : supercdms,
              'CRESST' : cresst,
              'Neutrino fog' : neutrino}

    return limits


def make_plot_SI(limits):
    print('Making SI limits plot.')

    fig, ax = plt.subplots(1,1,figsize = (6,4.5))

    #Xe
    limit_key = 'XENONnT'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
            ls = '-', label = limit_key, color = 'C0',
            zorder = 10)
    limit_key = 'LZ'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
                ls = '-', label = limit_key, color = 'C1')
    limit_key = 'PandaX-4T'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
                ls = '-', label = limit_key, color = 'C2')
    limit_key = 'XENON1T (2-fold)'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
                ls = '-', label = limit_key, color = 'C3')
    limit_key = 'XENON1T (S2-only)'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
                ls = '-', label = limit_key, color = 'C4')
    limit_key = 'DARWIN (projection)'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
                ls = '-', label = limit_key, color = 'C5')
    
    #Ar
    limit_key = 'DEAP-3600'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
            ls = '--', label = limit_key, color = 'C6')
    limit_key = 'Darkside-50_low'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
            ls = '--', label = 'Darkside-50', color = 'C7')
    limit_key = 'Darkside-50_high'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
            ls = '--', color = 'C7')

    #Other
    limit_key = 'DAMIC'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1],
            ls = '-.', label = limit_key, color = 'C8')
    limit_key = 'SuperCDMS'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1],
            ls = '-.', label = limit_key, color = 'C9')
    limit_key = 'CDMSLite'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1],
            ls = '-.', color = 'C9')
    limit_key = 'CRESST'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1],
            ls = '-.', label = limit_key, color = 'C10')

    limit_key = 'Neutrino fog'
    ax.fill_between(limits[limit_key][:,0],
                    0,
                    limits[limit_key][:,1],
                    ls = ':', label = limit_key, 
                    alpha = 0.7,
                    color = 'lightgrey')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e0,1e3)
    ax.set_ylim(1e-50,5e-37)

    ax.set_xlabel('WIMP Mass [GeV/c$^2$]')
    ax.set_ylabel('SI WIMP-nucleon cross section [cm$^2$]')
    ax.legend(ncol = 4,  loc = 'lower center', bbox_to_anchor=((0.5,1)))
    #fig.set_tight_layout(True)
    fig.savefig('Figures/limits_SI.pdf')

if __name__ == '__main__':

    limits = load_files_SI()
    make_plot_SI(limits)