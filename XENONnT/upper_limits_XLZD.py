import numpy as np
import matplotlib.pyplot as plt

from numpy import linspace, pi, sqrt, exp, zeros, size, shape, array, append, flipud, gradient
from numpy import trapz, interp, loadtxt, log10, log, savetxt, vstack, transpose
from numpy import ravel,tile,mean,inf,nan,amin,amax
from scipy.ndimage.filters import gaussian_filter1d
from scipy.integrate import cumtrapz
from numpy.linalg import norm
from scipy.special import gammaln

def load_files_SI():
    print('Loading csv files for SI WIMP-nucleon cross section!')

    xenon1t_SI = np.loadtxt("Data/limits/xenon1t_SI.csv",delimiter=",")
    cdms = np.loadtxt("Data/limits/CDMSLite2018_SI.csv",delimiter=",")
    cresst = np.loadtxt("Data/limits/CRESSTII_SI_2016_v2.csv",delimiter=",")
    damic = np.loadtxt("Data/limits/DAMIC_2020.csv",delimiter=",")
    darkside_low = np.loadtxt("Data/limits/darkside50_lowmass_ul.csv",delimiter=",")
    darkside_20k = np.loadtxt("Data/limits/DS_20k.csv",delimiter=",")
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
              'Darkside-20k' : darkside_20k,
              'DAMIC' : damic,
              'CDMSLite' : cdms,
              'SuperCDMS' : supercdms,
              'CRESST' : cresst,
              'Neutrino fog' : neutrino}

    return limits

def Floor_2D(data,filt=True,filt_width=3,Ex_crit=1e10):
    sig = data[1:,0]
    m = data[0,1:]
    n = size(m)
    ns = size(sig)
    Ex = flipud(transpose(data[1:,1:].T))
    Ex[Ex>Ex_crit] = nan
    Exmin = amin(Ex[Ex>0])
    Ex[Ex==0] = Exmin
    DY = zeros(shape=shape(Ex))
    for j in range(0,n):
        y = log10(Ex[:,j])
        if filt:
            y = gaussian_filter1d(gaussian_filter1d(y,sigma=3),filt_width)
            dy = gradient(y,log10(sig[2])-log10(sig[1]))
            dy = gaussian_filter1d(dy,filt_width)
        else:
            dy = gradient(y,log10(sig[2])-log10(sig[1]))

        DY[:,j] = dy
    NUFLOOR = zeros(shape=n)
    #for j in range(0,n):
    #    DY[:,j] = gaussian_filter1d(DY[:,j],filt_width)
    for j in range(0,n):
        for i in range(0,ns):
            if DY[ns-1-i,j]<=-2.0:
                i0 = ns-1-i
                i1 = i0+10
                NUFLOOR[j] = 10.0**interp(-2,DY[i0:i1+1,j],log10(sig[i0:i1+1]))
                DY[ns-1-i:-1,j] = nan
                break
    DY = -DY
    DY[DY<2] = 2
    return m,sig,NUFLOOR,DY

def plot_nu_floor(figax = None):
    if figax is None:
        fig,ax = plt.subplots(1,1,figsize=(7.4,5))
    else:
        fig,ax = figax

    vmax = 7
    vmin = 2.2
    data = loadtxt('Data/limits/DLNuFloorXe_detailed_SI.txt')
    m,sig,NUFLOOR,DY = Floor_2D(data,filt=True,filt_width=2,Ex_crit=1e10)
    cnt = ax.contourf(m,sig,DY,levels=linspace(2,15,100),vmax=vmax,vmin=vmin,cmap=cmap)
    ax.plot(m,NUFLOOR,'-',color='brown',lw=3,path_effects=pek,zorder=100)

    return fig,ax

def make_plot_SI_XLZD(limits):
    print('Making SI limits plot.')

    fig, ax = plt.subplots(1,1,figsize = (7.4,5))

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
                ls = '-', label = 'XENON1T (2-fold, S2-only)',
                color = 'C3')
    limit_key = 'XENON1T (S2-only)'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
                ls = '-',  color = 'C3')#, label = limit_key)
    limit_key = 'DARWIN (projection)'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
                ls = '-', label = limit_key, color = 'C4')
    
    #Ar
    limit_key = 'DEAP-3600'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
            ls = '--', label = limit_key, color = 'C5')
    limit_key = 'Darkside-50_low'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
            ls = '--', label = 'Darkside-50', color = 'C6')
    limit_key = 'Darkside-50_high'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
            ls = '--', color = 'C6')
    @np.vectorize
    def totheten(x):
        return 10**x
    
    limit_key = 'Darkside-20k'
    ax.plot(limits[limit_key][:,0],
            totheten(limits[limit_key][:,1]), 
            ls = '--', color = 'C7', 
            label = 'DarkSide-20k (projection)')

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
    fig.savefig('Figures/limits_SI_XLZD.pdf')


if __name__ == '__main__':

    limits = load_files_SI()
    #make_plot_SI_XLZD(limits)

    fig, ax = plot_nu_floor()
    plt.savefig('Figures/nu_floor_XLZD.pdf')