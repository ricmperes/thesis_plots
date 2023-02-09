import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as itp
from matplotlib.patches import Rectangle
from pylars.utils.common import Gaussian
from scipy.optimize import curve_fit


def plot_area_specturm(AreaValues, log = True, figax = None):
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (6,2))
    else:
        fig, ax = figax

    bins = np.linspace(0, 2e5, 800)

    ax.hist(AreaValues*10,bins = bins, label = 'no cuts', histtype = 'step')

    ax.set_xlabel('Pulse Area [integrated ADC counts]')
    ax.set_xlabel('# events')
    if log == True:
        ax.set_yscale('log')
        fig.savefig('Figures/quad_area_spectrum_log.pdf')
    else:
        fig.savefig('Figures/quad_area_spectrum.pdf')

def plot_length_cut_line(WidthValues, length_cut = 15, figax = None):
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (3,2))
    else:
        fig, ax = figax

    ax.hist(WidthValues, bins = np.arange(0,40), histtype = 'step')
    ax.axvline(15, ls = '--', 
        c = plt.rcParams['axes.prop_cycle'].by_key()['color'][1])
    ax.set_yscale('log')
    ax.set_xlim(3,40)
    ax.set_xlabel('Pulse Length [# samples]')
    
    fig.savefig('Figures/length_cut_histogram.pdf')
    plt.close()


def plot_length_cut_effect(AreaValues, WidthValues, figax = None):
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (3,2))
    else:
        fig, ax = figax

    bins = np.linspace(0, 2e5, 800)

    ax.hist(AreaValues*10,bins = bins, label = 'no cuts', histtype = 'step')

    [ax.hist(AreaValues[(AreaValues>0) & (WidthValues>_w)]*10,bins = bins, 
            histtype = 'step', 
            label =f'Length > {_w}') for _w in range(5,40,10)]

    ax.set_xlabel('Pulse Area [integrated ADC counts]')
    ax.set_yscale('log')
    ax.legend()

    fig.savefig('Figures/length_cut_effect.pdf')
    plt.close()

def plot_DCR_steps(area_hist_x, DCR_values, DCR_der_x_points, 
                   DCR_der_y_points, min_area_x, figax = None):
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (3,1.8))
    else:
        fig, ax = figax

    ax.plot(area_hist_x, DCR_values,
        marker='.', ls='', ms = 2,
        label='Data points', zorder = 7)
    ax.set_yscale('log')
    ax.set_xlabel('Area [integrated ADC counts]')
    ax.set_ylabel('# events')

    ax3 = ax.twinx()
    ax3.plot(DCR_der_x_points, -DCR_der_y_points/min(DCR_der_y_points), 
             zorder = 2, alpha = 0.7, 
             c = plt.rcParams['axes.prop_cycle'].by_key()['color'][1])

    ax3.tick_params(
        axis='y', 
        labelcolor=plt.rcParams['axes.prop_cycle'].by_key()['color'][1])

    ax3.axvline(min_area_x,ls='--', alpha=0.8,
                label='1$^{st}$ der. (smoothed)', zorder = 2, 
                c = plt.rcParams['axes.prop_cycle'].by_key()['color'][1])

    ax3.set_ylabel('1$^{st}$ derivative [a.u.]')
    fig.savefig('Figures/quad_DCR_steps.pdf')
    plt.close()

def plot_SPE_fit(AreaValues, WidthValues, A, mu, sigma, figax = None):
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (3,1.8))
    else:
        fig, ax = figax
    
    bins = np.linspace(0, 2e5, 800)

    _x = np.linspace(25e3, 75e3,500)
    ax.hist(AreaValues[(AreaValues>0) & (WidthValues>15)]*10,bins = bins, 
            histtype = 'step', label = 'Data in dark')

    ax.fill_between(_x, Gaussian(_x, A, mu, sigma), label = f'SPE fit')
    ax.set_xlabel('PeakArea')
    ax.set_yscale('log')

    ax.set_ylim(0.5,9e3)

    text1 = f'$\mu = ${mu:.2f}'
    text2 = f'$\sigma = ${sigma:.2f}'
    extra1 = Rectangle((0, 0), 1, 1, fc="w", fill=False, 
                       edgecolor='none', linewidth=0, label = text1)
    extra2 = Rectangle((0, 0), 1, 1, fc="w", fill=False, 
                       edgecolor='none', linewidth=0, label = text2)
    ax.add_patch(extra1)
    ax.add_patch(extra2)
    ax.legend()

    fig.savefig('Figures/quad_SPE_fit.pdf')
    plt.close()

def plot_cuts_quad():
    """All in one solution: cuts, SPE, DCR steps.
    """

    AreaValues = np.load('./Data/quad_AreaValues.npy')
    WidthValues = np.load('./Data/quad_WidthValues.npy')

    ## Area spectrum 
    plot_area_specturm(AreaValues, log = True)
    plot_area_specturm(AreaValues, log = False)

    ## Length cut
    plot_length_cut_line(WidthValues)
    plot_length_cut_effect(AreaValues, WidthValues)

    ## Prepare SPE an DCR
    bins = np.linspace(0, 2e5, 800)
    area_hist = np.histogram(AreaValues[(AreaValues>0) & (WidthValues>15)]*10,
                         bins=bins)
    area_hist_x = area_hist[1]
    area_hist_x = (area_hist_x +
                (area_hist_x[1] - area_hist_x[0]) / 2)[:-1]
    area_hist_y = area_hist[0]

    DCR_values = np.flip(np.cumsum(np.flip(area_hist_y)))
    grad = np.gradient(DCR_values)
    grad_spline = itp.UnivariateSpline(area_hist_x, grad)
    # , s = len(area_hist_x)*3)
    DCR_der_x_points = np.linspace(area_hist_x[0], area_hist_x[-1], 800)
    DCR_der_y_points = grad_spline(DCR_der_x_points)
    min_idx = np.where(DCR_der_y_points == min(DCR_der_y_points))
    min_area_x = DCR_der_x_points[min_idx][0]

    (A, mu, sigma), cov = curve_fit(Gaussian, area_hist_x, area_hist_y,
                                    p0=(2000, min_area_x, 0.05 * min_area_x))

    sigma = np.abs(sigma)
    ## Plot DCR steps and SPE rough
    plot_DCR_steps(area_hist_x, DCR_values, DCR_der_x_points, 
                   DCR_der_y_points, min_area_x)
    plot_SPE_fit(AreaValues, WidthValues, A, mu, sigma)


