import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.colors import LogNorm
from scipy.interpolate import CloughTocher2DInterpolator
import pandas as pd

def DCR_fit_func(x, a, b):
    ans = np.exp(a*x + b)
    return ans

def fit_DCR_data(df, xvar = 'Gain'):
    funcs_pars = {}
    for i, t in enumerate(np.unique(df['T'])):

        _mask = (df['T'] == t)
        if xvar == 'Gain':
            _x = np.log10(df[_mask][xvar])
        else:
            _x = df[_mask][xvar]
        par, cov = curve_fit(DCR_fit_func, 
                            _x, 
                            df[_mask]['DCR'])
        funcs_pars[t] = [*par]

    return funcs_pars

def get_interpolator(df,y_min, y_max,
                     yvar = 'Gain'):
    # Get fucntion from where to extrapolate values for unmeasured gains
    funcs_pars = fit_DCR_data(df, xvar=yvar)

    # Feed DCR values at (T, Gain) from the fit at each T
    _temps = np.unique(df['T']) #np.arange(170,201, 5)
    _gains = np.linspace(y_min,y_max,200)
    
    if yvar == 'Gain':
        that_z = np.array(
            [DCR_fit_func(np.log10(_gains), *funcs_pars[_t]) for _t in _temps])
    else:
        that_z = np.array(
            [DCR_fit_func(_gains, *funcs_pars[_t]) for _t in _temps])

    # Now with a lot of values at each temperature, make the interpolator
    _xx, _yy = np.meshgrid(_temps, _gains, indexing='ij')
    DCR_quad_2d = CloughTocher2DInterpolator((_xx.flatten(), _yy.flatten()), 
                                            that_z.flatten(),
                                            rescale=True)

    # The interpolater is done!
    return DCR_quad_2d


def plot_DCR_hitmap(df, ymin = 0.1e6, ymax = 6e6, yvar = 'Gain',
                    grid_size = 1000, contours:bool = True, 
                    figax = None, tag = ''):

    # Get the interpolator
    DCR_quad_2d = get_interpolator(df, y_min = ymin, y_max=ymax,
                                   yvar=yvar)
    print('Defined 2D interpolator')

    # Define grid
    _ts = np.unique(df['T'])
    _t_grid = np.linspace(min(_ts),max(_ts),grid_size)
    _g_grid = np.linspace(ymin,ymax,grid_size)
    _tt_grid, _gg_grid = np.meshgrid(_t_grid, _g_grid, indexing='ij')
    _zz_grid = DCR_quad_2d(_tt_grid, _gg_grid)

    # Make the plot
    print('Starting plot')
    if figax == None:
        fig, ax = plt.subplots(1,1,figsize = (6,4))

    ax.scatter(df['T'], df['Gain'], 
                c = 'white',marker = 'x', zorder = 1,
                alpha = 0.9,# fc='none', ec='white', 
                s = 20, label = 'Data measured')
    pmesh = ax.pcolormesh(_tt_grid, _gg_grid, _zz_grid, cmap='coolwarm', 
                        norm=LogNorm(), zorder = -1)

    contours = ax.contour(_tt_grid, _gg_grid, _zz_grid, 
                        [0.1,0.5,1,2,5,10,20], alpha = 0.9,
                        colors = 'k')
    ax.legend(loc='upper right')
    def fmt(x):
        return f'{x:.1f} Hz/mm$^2$'

    manual_locations = [(174, 1e6),(176,1.5e6),(173,3.3e6),
                    (177.5,3.9e6),(187,3.5e6),(193,4e6),(197,5e6)]

    ax.clabel(contours, contours.levels, inline=True, 
              manual = manual_locations, fmt = fmt, fontsize = 8)

    ax.grid(True, lw = 1, zorder = 5)
    fig.colorbar(pmesh,label = 'DCR [Hz/mm$^2$]')
    ax.set_ylabel('Gain')
    ax.set_xlabel('Temp [K]')

    fig.savefig(f'Figures/DCR_hitmap_{yvar}{tag}.jpeg')
    plt.close()

if __name__ == '__main__':

    # Load my style ;)
    plt.style.use('../thesis_style.mplstyle')
   
    df_quad = pd.read_hdf('Data/detail_study/quad_characterisation.h5')

    plot_DCR_hitmap(df = df_quad,
                    yvar = 'Gain',
                    grid_size = 1000,
                    tag = '_quad')
    df_tile = pd.read_hdf('Data/detail_study/tile_characterisation.h5')                    
    plot_DCR_hitmap(df = df_tile,
                    yvar = 'Gain',
                    grid_size = 1000,
                    tag = '_tile')