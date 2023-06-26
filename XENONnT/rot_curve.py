import matplotlib.pyplot as plt
import numpy as np

from scipy.interpolate import interp1d

def load_data():
    data = np.loadtxt('Data/NGC3198/NGC_3198_data.csv', delimiter=',')
    ans = data
    return ans

def load_curves():
    disk = np.loadtxt('Data/NGC3198/NGC_3198_disk.csv', delimiter=',')
    halo = np.loadtxt('Data/NGC3198/NGC_3198_halo.csv', delimiter=',')
    gas = np.loadtxt('Data/NGC3198/NGC_3198_gas.csv', delimiter=',')
    
    ans = {'Disk': disk, 'Gas': gas, 'Halo': halo,}
    return ans

def make_1d_curves(**curve_data):
    curves = {}
    for key, val in curve_data.items():
        curves[key] = interp1d(val[:,0], val[:,1], 
                               kind = 'linear',
                               fill_value='extrapolate')
    return curves


def main():
    print('Running')
    curves_data = load_data()
    curves_1d = make_1d_curves(**curves_data)

    print(curves_1d['disk'](10.0))

def plot_curves(figax = None):
    if figax is None:
        fig, ax = plt.subplots(1,1, figsize=(4,4))
    else:
        fig, ax = figax

    data = load_data()
    curves_points = load_curves()
    curves_1d = make_1d_curves(**curves_points)

    data_y_err_up = data[:,2]-data[:,1]
    data_y_err_down = data[:,1]-data[:,3]
    ax.errorbar(data[:,0], data[:,1], yerr=[data_y_err_down, data_y_err_up],
                marker = 'o', capsize=4,label = 'Data', ls = '',
                zorder = 10)
    
    r = np.linspace(1, 30, 400)
    for curve in curves_1d:
        ax.plot(r, curves_1d[curve](r), 
                marker = '', label=curve)
    curve_sum = (curves_1d['Disk'](r)**2 + 
                 curves_1d['Gas'](r)**2 + 
                 curves_1d['Halo'](r)**2)**0.5
    ax.plot(r, curve_sum, marker = '', label='Sum', color='k')

    ax.set_xlabel('Radius [kpc]')
    ax.set_ylabel('Velocity [km/s]')
    ax.set_xlim(1, 35)
    ax.set_ylim(0, 200)
    ax.legend()
    fig.savefig('Figures/rot_curve_all.png', bbox_inches='tight')
    
    if figax is None:
        plt.show()
    else:
        return fig, ax

if __name__ == '__main__':
    plt.style.use('../thesis_style.mplstyle')
    plot_curves()
