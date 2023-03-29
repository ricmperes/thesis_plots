import argparse

parser = argparse.ArgumentParser(
    description=('Redo Xenoscope plots.')
)
parser.add_argument('-p', '--properties',
                    help='Make properties plots.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-w', '--waveforms',
                    help='Make waveforms plots.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-c', '--cuts',
                    help='Make cuts plots.',
                    nargs='?', const=True,
                    default= False,
                    required=False)                                        
parser.add_argument('-l', '--LED',
                    help='Make LED plots.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-a', '--air',
                    help='Make plots of Top Array in air (Dec22).',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-t', '--total',
                    help='Make plots of all the 50 quads properties.',
                    nargs='?', const=True,
                    default= False,
                    required=False)
parser.add_argument('-s', '--spe',
                    help='Make plots of the spe comparison study.',
                    nargs='?', const=True,
                    default= False,
                    required=False)    
parser.add_argument('-xm', '--xenonmass',
                    help='Make plot of the xenon mass pressure in bottles.',
                    nargs='?', const=True,
                    default= False,
                    required=False)                       

args = parser.parse_args()

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import pylars

from properties_plots import *
from waveform_plots import *
from cut_plots import *
from LED_ON_plots import *
from air_plots import *
from all_quads_plots import *
from SPE_res_comparision_plots import *
from Xe_mass import make_xe_mass_plot

# Load my style ;)

plt.style.use('../thesis_style.mplstyle')

#the lovely coolwarm colormap :)

from matplotlib.colors import ListedColormap

cm = plt.cm.get_cmap('coolwarm')

# Get the colormap colors, multiply them with the factor "a", and create new colormap
a = 0.85
coolwarm = plt.cm.coolwarm(np.arange(plt.cm.coolwarm.N))
coolwarm[:,0:3] *= a 
coolwarm = ListedColormap(coolwarm)

summer = plt.cm.summer(np.arange(plt.cm.summer.N))
summer[:,0:3] *= a 
summer = ListedColormap(summer)

if __name__ == '__main__':

    plot_properties = args.properties
    plot_waveforms = args.waveforms
    plot_cuts = args.cuts
    plot_LED = args.LED
    plot_air = args.air
    plot_total = args.total
    plot_spe_compare = args.spe
    plot_xe_mass = args.xenonmass

    if plot_properties:
        print('Plotting properties of sensors')

        # ## 6x6 ##
        # df_6x6 = pd.read_hdf('Data/6x6_characterisation.h5')
        # BVs_6x6 = pylars.analysis.breakdown.compute_BV_DCRds_results(df_6x6, 
        #     plot = False)
        # plot_gain_v(df_6x6[df_6x6['V']< 56], coolwarm, 48, 56, '6x6_gain_v.pdf')
        # plot_bv_temp(BVs_6x6, 165, 215, '6x6_bv_temp.pdf')
        # plot_parameter_vs_gain(df_6x6,'SPE_res', 'SPE resolution [%]', 
        #                     'linear', coolwarm,
        #                     '6x6_errorbars', errorbars = True)
        # plot_parameter_vs_gain(df_6x6,'SPE_res', 'SPE resolution [%]', 
        #                     'linear', coolwarm,
        #                     '6x6_NOerrorbars', errorbars = False)
        # _df_6x6 = df_6x6[~(
        #     ((df_6x6['Gain']>1.7e6) & (df_6x6['T'] == 200)) | 
        #     ((df_6x6['Gain']>2.2e6) & (df_6x6['T'] == 190)))]
        # plot_parameter_vs_gain(_df_6x6,'DCR', 'DCR [Hz/mm$^2$]', 
        #                     'linear', coolwarm,
        #                     '6x6_errorbars', errorbars = True)
        # plot_parameter_vs_gain(df_6x6,'DCR', 'DCR [Hz/mm$^2$]', 
        #                     'linear', coolwarm,
        #                     '6x6_NOerrorbars', errorbars = False)
        # plot_parameter_vs_gain(df_6x6,'CTP', 'CTP [%]', 
        #                     'linear', coolwarm,
        #                     '6x6_errorbars', errorbars = True)
        # plot_parameter_vs_gain(df_6x6,'CTP', 'CTP [%]', 
        #                     'linear', coolwarm,
        #                     '6x6_NOerrorbars', errorbars = False)

        ## Quad ##
        print('Plotting quad')
        df_quad = pd.read_hdf('Data/detail_study/quad_characterisation.h5')
        BVs_quad = pylars.analysis.breakdown.compute_BV_DCRds_results(
            df_quad, plot = False)
        BVs_quad.style.to_latex('BVs_quad.txt',
                                label = 'tab:BV_xenoscope_quads', 
                                caption = ('Breakdown voltage for a quad at different temperatures.',
                                           'Breakdown voltage measured in a quad.'),
                                hrules = True,
                                position_float = 'centering',
                                position = 'h!')
        plot_gain_v(df_quad, coolwarm, 48, 56, 'quad_gain_v.pdf')
        plot_bv_temp(BVs_quad, 165, 215, 'quad_bv_temp.pdf')
        #plot_parameter_vs_gain(df_quad,'SPE_res', 'SPE resolution [%]', 
        #                    'linear', coolwarm,
        #                    'quad_errorbars', errorbars = True)
        #plot_parameter_vs_gain(df_quad,'SPE_res', 'SPE resolution [%]', 
        #                    'linear', coolwarm,
        #                    'quad_NOerrorbars', errorbars = False)
        #plot_parameter_vs_gain(df_quad,'DCR', 'DCR [Hz/mm$^2$]', 
        #                    'linear', coolwarm,
        #                    'quad_errorbars', errorbars = True)
        #plot_parameter_vs_gain(df_quad,'DCR', 'DCR [Hz/mm$^2$]', 
        #                    'linear', coolwarm,
        #                    'quad_NOerrorbars', errorbars = False)
        #plot_parameter_vs_gain(df_quad,'CTP', 'CTP [%]', 
        #                    'linear', coolwarm,
        #                    'quad_errorbars', errorbars = True)
        #plot_parameter_vs_gain(df_quad,'CTP', 'CTP [%]', 
        #                    'linear', coolwarm,
        #                    'quad_NOerrorbars', errorbars = False)
        ## Tile ##
        print('Plotting tile')
        df_tile = pd.read_hdf('Data/detail_study/tile_characterisation.h5')
        BVs_tile = pylars.analysis.breakdown.compute_BV_DCRds_results(
            df_tile, plot = False)
        BVs_tile.style.to_latex('BVs_tile.txt',
                                label = 'tab:BV_xenoscope_quads', 
                                caption = ('Breakdown voltage for a tile at different temperatures.',
                                           'Breakdown voltage measured for a tile.'),
                                hrules = True,
                                position_float = 'centering',
                                position = 'h!')
        plot_gain_v(df_tile, coolwarm, 48, 56, 'tile_gain_v.pdf')
        plot_bv_temp(BVs_tile, 165, 215, 'tile_bv_temp.pdf')

        df_tile = df_tile[df_tile['T'] <= 200]
        #plot_parameter_vs_gain(df_tile,'SPE_res', 'SPE resolution [%]', 
        #                    'linear', coolwarm,
        #                    'tile_errorbars', errorbars = True)
        # plot_parameter_vs_gain(df_tile,'SPE_res', 'SPE resolution [%]', 
        #                     'linear', coolwarm,
        #                     'tile_NOerrorbars', errorbars = False)
        #plot_parameter_vs_gain(df_tile,'DCR', 'DCR [Hz/mm$^2$]', 
        #                    'linear', coolwarm,
        #                    'tile_errorbars', errorbars = True)
        # plot_parameter_vs_gain(df_tile,'DCR', 'DCR [Hz/mm$^2$]', 
        #                     'linear', coolwarm,
        #                     'tile_NOerrorbars', errorbars = False)
        #plot_parameter_vs_gain(df_tile,'CTP', 'CTP [%]', 
        #                    'linear', coolwarm,
        #                    'tile_errorbars', errorbars = True)
        # plot_parameter_vs_gain(df_tile,'CTP', 'CTP [%]', 
        #                     'linear', coolwarm,
        #                     'tile_NOerrorbars', errorbars = False)

        plot_parameter_vs_gain_both(df_quad, df_tile ,
                                'SPE_res', 'SPE resolution [%]', 
                                'linear', coolwarm, summer,
                                'both', errorbars = True)
        plot_parameter_vs_gain_both(df_quad, df_tile ,
                                'DCR', 'DCR [Hz/mm$^2$]', 
                                'linear', coolwarm, summer,
                                'both', errorbars = True)
        plot_parameter_vs_gain_both(df_quad, df_tile ,
                                'DCR', 'DCR [Hz/mm$^2$]', 
                                'log', coolwarm, summer,
                                'both', errorbars = True)
        plot_parameter_vs_gain_both(df_quad, df_tile ,
                                'CTP', 'CTP [%]', 
                                'linear', coolwarm, summer,
                                'both', errorbars = True)

    if plot_waveforms:
        print('Making waveforms plot.')

        fig, ax = plt.subplots(1,1,figsize = (6,2))
        fig, ax = plot_wf_PEs(figax = (fig, ax))
        fig.savefig('Figures/waveform_PE.pdf')
        plt.close()

        fig, ax = plt.subplots(1,1,figsize = (6,2))
        fig, ax = plot_wf_LED(figax = (fig, ax))
        fig.savefig('Figures/waveform_LED.pdf')
        plt.close()

        fig, ax = plt.subplots(1,1,figsize = (6,2))
        fig, ax = plot_wf_LED_stacked(figax = (fig, ax))
        fig.savefig('Figures/waveform_LED_stacked.pdf')
        plt.close()

    if plot_cuts:
        print('Plotting cut effects.')
        plot_cuts_quad()

    if plot_LED:
        print('Plotting LED data.')
        plot_LED_aqueduct_and_BV(coolwarm)

    if plot_air:
        print('Plotting Xenoscope air data.')
        plot_BV_in_air()
        plot_light_levels()
    
    if plot_total:
        print('Plotting 50 quad distributions.')
        plot_BV_all_quads_hybrid()
        
        plot_prop_all_quads_hybrid('Gain', ylabel = 'Gain')
        plot_prop_all_quads_hybrid('DCR', ylabel = 'DCR [Hz/mm$^2$]')
        plot_prop_all_quads_hybrid('CTP', ylabel = 'CTP [%]')
        plot_prop_all_quads_hybrid('SPE_res', ylabel = 'SPE resolution [%]')
        
    if plot_spe_compare:
        plot_PMT_SiPM_dif()
        plot_PMT_SiPM_spectrums()

    if plot_xe_mass:
        make_xe_mass_plot()