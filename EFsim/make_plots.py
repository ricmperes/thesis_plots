import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pykefield as pkf
import scipy.interpolate as itp
from matplotlib.patches import Rectangle

# Load my style ;)

plt.style.use('/home/atp/rperes/notebooks/thesis_plots/thesis_style.mplstyle')

#the lovely coolwarm colormap :)

from matplotlib.colors import ListedColormap

cm = mpl.colormaps.get_cmap('coolwarm')

# Get the colormap colors, multiply them with the factor "a", 
# and create new colormap
a = 0.85
coolwarm = plt.cm.coolwarm(np.arange(plt.cm.coolwarm.N))
coolwarm[:,0:3] *= a 
coolwarm = ListedColormap(coolwarm)

summer = plt.cm.summer(np.arange(plt.cm.summer.N))
summer[:,0:3] *= a 
summer = ListedColormap(summer)


def build_func3d(arrays_3d):
    xxx, yyy, zzz, Phi_array, Ex, Ey, Ez, Emod_array = arrays_3d
    Phi_3d = itp.RegularGridInterpolator((xxx[:,0,0],yyy[0,:,0], zzz[0,0,:]), 
                                         Phi_array,bounds_error=False, 
                                         fill_value=np.nan, method = 'linear')
    Emod_3d = itp.RegularGridInterpolator((xxx[:,0,0],yyy[0,:,0], zzz[0,0,:]), 
                                         Emod_array,bounds_error=False, 
                                         fill_value=np.nan)
    Ex_3d = itp.RegularGridInterpolator((xxx[:,0,0],yyy[0,:,0], zzz[0,0,:]), 
                                         Ex,bounds_error=False, 
                                         fill_value=np.nan)
    Ey_3d = itp.RegularGridInterpolator((xxx[:,0,0],yyy[0,:,0], zzz[0,0,:]), 
                                         Ey,bounds_error=False, 
                                         fill_value=np.nan)
    Ez_3d = itp.RegularGridInterpolator((xxx[:,0,0],yyy[0,:,0], zzz[0,0,:]), 
                                         Ez,bounds_error=False, 
                                         fill_value=np.nan)
    Phi_3d.name = 'Phi'
    Emod_3d.name = 'Emod'
    Ex_3d.name = 'Ex'
    Ey_3d.name = 'Ey'
    Ez_3d.name = 'Ez'
    func_3d = Phi_3d,Ex_3d,Ey_3d,Ez_3d,Emod_3d
    
    return func_3d

def load_3d_arrays():
    xxx = np.load('data/xxx.npy')
    yyy = np.load('data/yyy.npy')
    zzz = np.load('data/zzz.npy')
    Phi_array = np.load('data/Phi_array.npy')
    Ex = np.load('data/Ex.npy')
    Ey = np.load('data/Ey.npy')
    Ez = np.load('data/Ez.npy')
    Emod_array = np.load('data/Emod_array.npy')
    arrays_3d = xxx,yyy,zzz, Phi_array ,Ex,Ey,Ez, Emod_array

    return arrays_3d

def load_mean_arrays():
    rr2 = np.load('data/rr2.npy')
    zz = np.load('data/zz.npy')
    Ex_mean = np.load('data/Ex_mean.npy')
    Ey_mean = np.load('data/Ey_mean.npy')
    Ez_mean = np.load('data/Ez_mean.npy')
    Emod_mean = np.load('data/Emod_mean.npy')
    Phi_mean = np.load('data/Phi_mean.npy')
    arrays_mean = rr2, zz, Ex_mean, Ey_mean, Ez_mean, Emod_mean, Phi_mean
    return arrays_mean

def plot_3dpotential(Phi_3d):
    fig = plt.figure(figsize = (5, 4))
    # gs = fig.add_gridspec(1, 2,  width_ratios=(15, 1),
    #                  left=0.1, right=0.9, bottom=0.1, top=0.9,
                    #   wspace=0.3)#, hspace=0.05)
    # ax = fig.add_subplot(gs[0, 0], projection='3d')
    # ax2 = fig.add_subplot(gs[0, 1])
    ax = fig.add_subplot(projection = '3d')

    fig, ax  = pkf.plot_fieldmap.plot_xy_slice(_x_set = 0,_y_set = 0, 
                                               func = Phi_3d,
                                               #axcbar = ax2, 
                                               cbar_on = False,
                                               save_fig = False, 
                                               figax = (fig, ax))
    #fig.tight_layout()
    fig.savefig('Figures/Phi_3d.png', dpi = 200)
    plt.close()
    

def plot_2dpotential(rr2, zz, Phi_mean):
    fig = plt.figure(figsize = (5, 4))
    ax = fig.add_subplot(111)
    fig, ax = pkf.plot_fieldmap.plot_average_phi(rr2, zz, Phi_mean, 
                                                 figax = (fig, ax),
                                                 save_fig=False)
    fig.savefig('Figures/Phi_2d.png', dpi = 200)
    plt.close()

def get_df_meanfield(rr2, zz, Ex_mean, Ey_mean, Ez_mean, Emod_mean, Phi_mean):
    df_meanfield = pd.DataFrame({'r2':rr2.ravel(), 
                                 'z':zz.ravel(), 
                                 'Ex':Ex_mean.ravel('F') ,
                                 'Ey':Ey_mean.ravel('F') , 
                                 'Ez':Ez_mean.ravel('F') , 
                                 'Phi':Phi_mean.ravel('F') ,
                                 'Emod':Emod_mean.ravel('F') })
                                 
    return df_meanfield

def plot_3d_efield(rr2, zz, Ex_mean, Ey_mean, Ez_mean, df_meanfield):
    fig, ax = plt.subplots(1,1,figsize = (4,4))
    fig, ax = pkf.plot_fieldmap.plot_average_efield(
        rr2 = rr2, 
        zz = zz, 
        EE = Ez_mean,
        df_meanfield = df_meanfield, 
        efieldtype = 'Ez',
        fidcolor = True,
        figax = (fig, ax),
        colorlabel = '$E_z$ [V/cm]',
        save_fig = False)
    fig.savefig('Figures/Ez_2d.png', dpi = 200)
    plt.close()

    fig, ax = plt.subplots(1,1,figsize = (4,4))
    fig, ax = pkf.plot_fieldmap.plot_average_efield(
        rr2 = rr2, 
        zz = zz, 
        EE = Ex_mean,
        df_meanfield = df_meanfield, 
        efieldtype = 'Ex',
        fidcolor = False,
        figax = (fig, ax),
        colorlabel = '$E_x$ [V/cm]',
        save_fig = False)
    fig.savefig('Figures/Ex_2d.png', dpi = 200)
    plt.close()

    fig, ax = plt.subplots(1,1,figsize = (4,4))
    fig, ax = pkf.plot_fieldmap.plot_average_efield(
        rr2 = rr2, 
        zz = zz, 
        EE = Ey_mean,
        df_meanfield = df_meanfield, 
        efieldtype = 'Ey',
        fidcolor = False,
        figax = (fig, ax),
        colorlabel = '$E_y$ [V/cm]',
        save_fig = False)
    fig.savefig('Figures/Ey_2d.png', dpi = 200)
    plt.close()


def plot_2d_streamlines(func_3d, Phi_3d):
    streamlist_xzplane = pkf.process_streamlines.make_streamlist_xzplane(
        func_3d)
    
    fig, ax = plt.subplots(1,1,figsize = (5,4))
    
    fig, ax = pkf.plot_streamlines.plot_2dstreamlines(Phi_3d, 
                                                      streamlist_xzplane, 
                                                      figax = (fig, ax))
    
    fig.savefig('Figures/streamlines_2d.png', dpi=200)
    plt.close()

def plot_3d_streamlines(func_3d,N_r,N_theta):
    streamlist = pkf.process_streamlines.make_streamlist_radial(
        N_r = N_r, N_theta = N_theta, func_3d = func_3d)
    fig = plt.figure(figsize = (5, 4))
    ax = fig.add_subplot(projection = '3d')

    fig, ax = pkf.plot_streamlines.plot_3dstreamlines(
        streamlist,
        linecolor = plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
        figax=(fig, ax))

    fig.savefig('Figures/streamlines_3d.png', dpi=200)
    plt.close()

if __name__ == '__main__':
    # Init 3D stuff
    print('Starting EFsim plots.')
    arrays_3d = load_3d_arrays()
    print('Arrays loaded.')
    func_3d = build_func3d(arrays_3d)
    print('3D functions ready.')
    Phi_3d,Ex_3d,Ey_3d,Ez_3d,Emod_3d = func_3d

    # Init 2D stuff
    arrays_mean = load_mean_arrays()
    rr2, zz, Ex_mean, Ey_mean, Ez_mean, Emod_mean, Phi_mean = arrays_mean
    df_meanfield = get_df_meanfield(rr2, zz, Ex_mean, Ey_mean, Ez_mean, 
                                    Emod_mean, Phi_mean)
    print('Mean field arrays loaded.')

    # Do plots
    plot_3dpotential(Phi_3d)
    plot_2dpotential(rr2, zz, Phi_mean)
    plot_3d_efield(rr2, zz, Ex_mean, Ey_mean, Ez_mean, df_meanfield)
    plot_2d_streamlines(func_3d[1:], Phi_3d)
    plot_3d_streamlines(func_3d[1:], N_r = 4, N_theta = 8)