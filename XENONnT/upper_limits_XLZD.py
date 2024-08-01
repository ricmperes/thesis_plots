import matplotlib as mpl
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt

from numpy import linspace, pi, sqrt, exp, zeros, size, shape, array, append, flipud, gradient
from numpy import trapz, interp, loadtxt, log10, log, savetxt, vstack, transpose
from numpy import ravel,tile,mean,inf,nan,amin,amax
from scipy.ndimage.filters import gaussian_filter1d
from scipy.integrate import cumtrapz
from numpy.linalg import norm
from scipy.special import gammaln
from scipy.interpolate import make_interp_spline

cm = mpl.colormaps.get_cmap('Greys')

# Get the colormap colors, multiply them with the factor "a", 
# and create new colormap
#a = 1
#cmap = plt.cm.Greys(np.arange(plt.cm.Greys.N))
#cmap = np.clip(cmap[:,0:3] * a,0,1)
#cmap = ListedColormap(cmap)

original_cmap = plt.cm.Greys  # Replace with your original cmap if different
new_colors = original_cmap(np.linspace(0, 0.8, 256))  # Use only the first half
cmap = ListedColormap(new_colors)


plt.style.use('/home/atp/rperes/notebooks/thesis_plots/thesis_style.mplstyle')

def load_files_SI():
    print('Loading csv files for SI WIMP-nucleon cross section!')

    xenon1t_SI = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/xenon1t_SI.csv",delimiter=",")
    cdms = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/CDMSLite2018_SI.csv",delimiter=",")
    cresst = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/CRESSTII_SI_2016_v2.csv",delimiter=",")
    damic = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/DAMIC_2020.csv",delimiter=",")
    darkside_low = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/darkside50_lowmass_ul.csv",delimiter=",")
    darkside_20k = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/DS_20k.csv",delimiter=",")
    darwin = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/darwin_SI.csv",delimiter=",")
    deap = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/Deap_SI_2018.csv",delimiter=",")
    lux = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/lux_SI.csv",delimiter=",")
    lz = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/LZ_SI.csv",delimiter=",")
    neutrino = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/neutrino_fog_SI.csv",delimiter=",")
    pandax = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/pandax4t_SI.csv",delimiter=",")
    xenonnt = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/xenonnt_SI.csv",delimiter=",")
    xenon1t_2fold = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/xenon1t_2fold_SI.csv",delimiter=",")
    xenon1t_s2only = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/xenon1t_s2only_SI.csv",delimiter=",")
    supercdms = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/SuperCDMS_SI.csv",delimiter=",")
    darkside_high = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/DS-50.csv",delimiter=",")
    xlzd200 = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/XLZD_200ty.csv",delimiter=",")
    xlzd1000 = np.loadtxt("/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/XLZD_1000ty.csv",delimiter=",")

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
              'Neutrino fog' : neutrino,
              'XLZD200' : xlzd200,
              'XLZD1000' : xlzd1000}

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
    
    vmax = 5
    vmin = 2
    #cmap = 'coolwarm'

    data = loadtxt('/home/atp/rperes/notebooks/thesis_plots/XENONnT/Data/limits/DLNuFloorXe_detailed_SI.txt')
    m,sig,NUFLOOR,DY = Floor_2D(data,filt=True,filt_width=2,Ex_crit=1e10)
    #cnt = ax.contourf(m,sig,DY,levels=linspace(0,3,50),
    #                  vmax=vmax,vmin=vmin,cmap=cmap)

    _xx, _yy = np.meshgrid(m, sig)
    sct = ax.scatter(_xx, _yy,c = DY,#levels=linspace(1.5,11,100),
                      vmax=vmax,vmin=vmin, 
                      cmap=cmap,
                      s=2,marker = 's',rasterized=False,alpha = 0.9)
    #_x = [m[0],m[-1]]
    ax.fill_between(x = m,y1=np.zeros(len(m)),y2=NUFLOOR,
                    color='grey',zorder=100, alpha = 0.15,)
                    #label = 'Neutrino fog')
    ax.plot(m,NUFLOOR,color='grey',
            zorder=100, alpha = 1, lw = 1,
            label = 'Neutrino floor')
    

    return fig,ax, sct

def make_plot_SI_XLZD(limits):
    print('Making SI limits plot.')

    fig, ax = plt.subplots(1,1,figsize = (7.4,4.5))

    @np.vectorize
    def totheten(x):
        return 10**x
    
    #Xe
    limit_key = 'XENONnT'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
            ls = '-', label = limit_key, color = 'C0',
            zorder = 10, lw = 2)
    limit_key = 'LZ'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
                ls = '-', label = limit_key, color = 'C1')
    limit_key = 'PandaX-4T'
    ax.plot(limits[limit_key][:,0],limits[limit_key][:,1], 
                ls = '-', label = limit_key, color = 'C2',
                lw = 2)

    limit_key = 'XLZD200'
    ax.plot(limits[limit_key][:,0],totheten(limits[limit_key][:,1]), 
                ls = '--', label = 'XLZD (200 ty)', color = 'C3',
                lw = 2)
    
    limit_key = 'XLZD1000'
    ax.plot(limits[limit_key][:,0],totheten(limits[limit_key][:,1]), 
                ls = '--', label = 'XLZD (1000 ty)', color = 'C4',
                lw = 2)
    

    # limit_key = 'Neutrino fog'
    # ax.fill_between(limits[limit_key][:,0],
    #                 0,
    #                 limits[limit_key][:,1],
    #                 ls = ':', label = limit_key, 
    #                 alpha = 0.7,
    #                 color = 'lightgrey')

    fig, ax, sct = plot_nu_floor(figax=(fig,ax))

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(5e0,1e4)
    ax.set_ylim(6e-50,1e-45)

    ax.set_xlabel('WIMP Mass [GeV/c$^2$]')
    ax.set_ylabel('SI WIMP-nucleon cross section [cm$^2$]')
    ax.legend(ncol = 3, columnspacing = 2,
              loc = 'lower center', bbox_to_anchor=((0.5,1)))
    #fig.set_tight_layout(True)
    fig.colorbar(sct, ax = ax, 
                 label = 'Gradient of discovery limit, $n$',
                 extend='both')
    fig.savefig('Figures/limits_SI_XLZD.jpeg', dpi = 300)


if __name__ == '__main__':

    limits = load_files_SI()
    #make_plot_SI_XLZD(limits)

    # fig, ax = plot_nu_floor()
    make_plot_SI_XLZD(limits)
    #plt.savefig('Figures/nu_floor_XLZD.jpeg')