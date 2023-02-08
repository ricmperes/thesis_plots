import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as itp
from matplotlib.patches import Rectangle
from pylars.utils.common import func_linear
from scipy.optimize import curve_fit
import pylars


# So I'm gonna use the data on farm, looking into putting it in a git lfs
# at some point, no time now, sorry. - 08.02.2023

def plot_LED_aqueduct_and_BV(cmap):
    base_run = pylars.utils.input.run(
        run_number=6, F_amp = 200,
        main_data_path='/disk/gfs_atp/xenoscope/SiPMs/char_campaign/raw_data/')

    process = pylars.processing.rawprocessor.run_processor(
            base_run, 'simple', sigma_level=5, baseline_samples=50)

    BV_ds = pylars.analysis.breakdown.BV_dataset(run = base_run,
                                                 processor=process,
                                                 temperature = 195,
                                                 module = 1,
                                                 channel = 'wf1')
    BV_ds.load_processed_data()

    select = BV_ds.voltages >= 47
    Vs = BV_ds.voltages[select]

    fig, ax = plt.subplots(1,1, figsize = (3.5,3))

    for i, _v in enumerate(Vs):
        if (_v*10)%5 != 0:
            continue
        try:
            df = BV_ds.data[_v]
        except:
            continue
        _cuts = ((df['position'] >= 290) & 
                 (df['position'] <= 310) & 
                 (df['length'] > 20))
        ax.hist(df[_cuts]['area'], bins = np.linspace(0,2.5e6, 500), 
                histtype = 'step', label = f'{_v} V', 
                color = cmap(i/len(Vs)))
        _med = np.median(df[_cuts]['area'])
        ax.axvline(_med, color = cmap(i/len(Vs)), ls = '--')

    ax.set_ylabel('# events')
    ax.set_xlabel('Pulse Area [ADC counts]')
    ax.set_yscale('log')
    ax.set_ylim(1,1e4)
    ax.legend(ncol=2, facecolor="white", framealpha = 0.8)

    fig.savefig('Figures/LED_aqueduct.pdf')
    plt.close()

    meds = []
    stds = []
    for i, _v in enumerate(Vs):
        df = BV_ds.data[_v]
        _cuts = ((df['position'] >= 290) & 
                 (df['position'] <= 310) & (df['length'] > 20))
        meds.append(np.median(df[_cuts]['area']))
        stds.append(np.std(df[_cuts]['area']))

    fig, ax = plt.subplots(1,1, figsize = (2.5,3))
    ax.errorbar(Vs, meds, yerr=stds,marker = 'x', ls = '')

    # Lin fit
    par, cov = curve_fit(func_linear, Vs[6:], meds[6:], 
        sigma=1/np.array(stds[6:])**2)
    _x = np.linspace(47, 53, 2)
    ax.plot(_x, func_linear(_x, *par), ls = '-', marker = '')

    ax.set_xlabel('Bias Voltage [V]')
    ax.set_ylabel('Median Pulse Area [ADC counts]')
    ax.set_ylim(0,1.8e6)
    ax.set_xlim(46.9,52)
    fig.savefig('Figures/LED_BV.pdf')
    plt.close()