"""Code adapted from https://github.com/NESTCollaboration/nestpy/blob/master/tutorials/arxiv/nestpy_tutorial.ipynb
"""

import matplotlib.pyplot as plt
import nestpy
import numpy as np
import scipy.interpolate as itp

detector = nestpy.DetectorExample_XENON10()
nc = nestpy.NESTcalc(detector)
A = 131.293 # avg atomic mass of Xe
Z = 54. # Atomic number of Xe 
density = nc.GetDensity( T=detector.get_T_Kelvin(), 
                        P=detector.get_p_bar(), inGas=False )
# these mean we don't compute photon times. 
# it's a bit more crude but over 100x faster. 
# So always do for a first-order approximation. 
S1mode = nestpy.S1CalculationMode.Hybrid   #Options are Full, Parametric, Hybrid, or Waveform
S2mode = nestpy.S2CalculationMode.Full     #Options are Full, or Waveform
output_timing = 0
wftime = [0, 0, 0]
wfamp = [0., 0., 0.]

def calc_Wq(density=density):
    #Using new W bindings
    W = nc.WorkFunction( rho=density )
    return W.Wq_eV

lifetime = detector.get_eLife_us() # us
#FreeParam = nestpy.default_nrer_widths_params()
FudgeFactor = [1,1]# FreeParam[4:6]
Wq_eV = calc_Wq(density=density)
g1 = detector.get_g1()
g2_params = nc.CalculateG2(False)
g2 = g2_params[3]


@np.vectorize
def get_drift_v(field, temp=177.15):
    dv = nc.SetDriftVelocity(temp, # K temp
                            density,
                            field)
    return dv

#Calculate the work function ev/quanta 
# This is done in nest but I found it simpler
# To just transcribe it here since there is no 
# Dependence except density. 
def calc_Wq(density=density):
    MolarMass = 131.293
    NEST_AVO = 6.0221409e23
    ATOM_NUM = 54.
    eDensity = ( density / MolarMass ) * NEST_AVO * ATOM_NUM
    Wq_eV = 20.7 - 1.01e-23 * eDensity
    
    return Wq_eV

def calc_Wq(density=density):
    #Using new W bindings
    W = nc.WorkFunction( rho=density )
    return W.Wq_eV

# This function gets both S1 and S2 for reliable anticorrelation.
@np.vectorize
def GetS1_S2(interaction=nestpy.NR, 
              energy=100., # energy in keV of the recoil itself
              drift_field=81.): # V/cm

    y = nc.GetYields(interaction,
     energy,
     density,
     drift_field,
     A,
     Z,
    ) 

    q = nc.GetQuanta(y, density)

    driftv = get_drift_v(drift_field)
    dv_mid = get_drift_v(drift_field) #assume uniform field 
    maxposz = 560 # max z position in mm  
    #We'll randomly select some positions to get realistic xyz smearing. 
    random_r = np.sqrt(np.random.uniform(0, 200.**2)) 
    random_theta = np.random.uniform(0, 2*np.pi)
    truthposx, truthposy, truthposz = random_r*np.cos(random_theta), random_r*np.sin(random_theta),np.random.uniform(60., 540.)
    smearposx, smearposy, smearposz = truthposx, truthposy, truthposz # random positions?
    
    dt = np.abs((truthposz - maxposz)/driftv)
    S1 = nc.GetS1(q, truthposx, truthposy, truthposz,
                        smearposx, smearposy, smearposz,
                        driftv, dv_mid, # drift velocities (assume homogeneous drift field)
                        interaction, 1, #int type, event # 
                        drift_field, energy, #dfield, energy
                        S1mode, output_timing,
                        wftime,
                        wfamp)

    S2 = nc.GetS2(q.electrons, 
                    truthposx, truthposy, truthposz,
                    smearposx, smearposy, smearposz,
                    dt, driftv, 1, #evt num
                    drift_field, S2mode, output_timing, # dv dvmid 
                    wftime, wfamp, 
                    g2_params)
    
    # S1[7] is the spike area, corrected for xyz position, and dividing out dpe effect.
    # S2[7] here is cs2_b, again correcting for DPE, xyz position, DAQ smearing
    cs1 = S1[7] 
    cs2 = S2[7]
    return cs1, cs2
def cut(s1, s2, 
        s1_acc=1, s2_acc=100, 
        s1_max=100):
    mask = np.logical_and(s1>s1_acc, s2>s2_acc)
    mask &= s1<=s1_max
    return s1[mask], s2[mask]

def plot_bands(field, s1_er, s2_er, s1_nr, s2_nr, smooth_er, smooth_nr):
    plot_bands_simple(field, s1_er, s2_er, s1_nr, s2_nr, smooth_er, smooth_nr)
    ##S2/S1 vs S1
    plot_bands_ratio(field, s1_er, s2_er, s1_nr, s2_nr, smooth_er, smooth_nr)

def plot_bands_ratio(field, s1_er, s2_er, s1_nr, s2_nr, smooth_er, smooth_nr):
    fig, ax = plt.subplots(1,1,figsize = (4,3))
    ax.scatter(s1_er, np.log10(s2_er/s1_er), s = 2, label='ER',alpha=0.03)
    ax.scatter(s1_nr, np.log10(s2_nr/s1_nr), label='NR',s=2,  alpha=0.03)

    _x = np.linspace(0,100,300)
    ax.plot(_x, np.log10(smooth_er(_x)/_x.T.flatten()), color = 'C2', lw = 1.5,)
    ax.plot(_x, np.log10(smooth_nr(_x)/_x.T.flatten()), color = 'C2', lw = 1.5,)

    ax.set_xlabel('S1 [pe]')
    ax.set_ylabel('log10(cs2/cs1)')
    ax.set_xlim(5, 100)
    ax.set_ylim(1.3,3)
    fig.savefig(f'Figures/bands_ratio_{field}.png')

def plot_bands_simple(field, s1_er, s2_er, s1_nr, s2_nr, smooth_er, smooth_nr):
    fig, ax = plt.subplots(1,1,figsize = (4,3))
    ax.scatter(s1_er, s2_er, s = 2, label='ER',alpha=0.03)
    ax.scatter(s1_nr, s2_nr, label='NR',s=2,  alpha=0.03)

    _x = np.linspace(0,100,300)
    ax.plot(_x, smooth_er(_x), c = 'C2', lw = 1.5,label = 'ER median')
    ax.plot(_x, smooth_nr(_x), c = 'C2', lw = 1.5,label = 'NR median')

    ax.set_xlabel('S1 [pe]')
    ax.set_ylabel('S2 [pe]')
    ax.set_yscale('log')
    ax.set_xlim(5, 100)
    ax.set_ylim(2e2,5e4)
    fig.savefig(f'Figures/bands_simple_{field}.png')

def run_sim(field, E_er, E_nr):
    print('Starting simulation')
    s1_er, s2_er = GetS1_S2(nestpy.beta, E_er, field)
    s1_er, s2_er = cut(s1_er, s2_er)
    print('ER sim finished')
    s1_nr, s2_nr = GetS1_S2(nestpy.nr, E_nr, field)
    s1_nr, s2_nr = cut(s1_nr, s2_nr)
    print('NR sim finished')
    return s1_er,s2_er,s1_nr,s2_nr

def get_smooth_lines(bin_center, s2_er_med, s2_nr_med):
    mask = ~np.isnan(s2_er_med)
    x_clean = bin_center[mask]
    y_clean = s2_er_med[mask]
    smooth_er = itp.UnivariateSpline(x_clean, y_clean, s = 5000000)

    mask = ~np.isnan(s2_nr_med)
    x_clean = bin_center[mask]
    y_clean = s2_nr_med[mask]
    smooth_nr = itp.UnivariateSpline(x_clean, y_clean, s = 200000)
    return smooth_er,smooth_nr

def divide_in_bins(s1_er, s2_er, s1_nr, s2_nr):
    x_min = 0,
    x_max = 100
    n_bins = 200
    bin_edge_minus = np.linspace(x_min, x_max, n_bins)
    bin_edge_plus = bin_edge_minus+(bin_edge_minus[1]-bin_edge_minus[0])
    bin_center = bin_edge_minus + (bin_edge_minus[1]-bin_edge_minus[0])/2
    
    s2_er_med = np.zeros(n_bins)
    s2_nr_med = np.zeros(n_bins)

    for bin_i in range(n_bins):
        #ER
        _mask = (s1_er > bin_edge_minus[bin_i]) & (s1_er < bin_edge_plus[bin_i])
        s2_er_med[bin_i] = np.median(s2_er[_mask])
        
        #NR
        _mask = (s1_nr > bin_edge_minus[bin_i]) & (s1_nr < bin_edge_plus[bin_i])
        s2_nr_med[bin_i] = np.median(s2_nr[_mask])
    return bin_center,s2_er_med,s2_nr_med
    
def make_band_plot(field):
    


    N = 100000
    E_er_max = 50. 
    E_nr_max = 100.

    E_er = np.random.uniform(0.1, E_er_max, N)
    E_nr = np.random.uniform(0.1, E_nr_max, N)
    field = field

    s1_er, s2_er, s1_nr, s2_nr = run_sim(field, E_er, E_nr)

    # divide in bins
    bin_center, s2_er_med, s2_nr_med = divide_in_bins(s1_er, s2_er, s1_nr, s2_nr)
    #Smooth lines
    smooth_er, smooth_nr = get_smooth_lines(bin_center, s2_er_med, s2_nr_med)

    #Make plots
    ## S2 vs s1
    plot_bands(field, s1_er, s2_er, s1_nr, s2_nr, smooth_er, smooth_nr)

if __name__=='__main__':
    print('Making band plot, 20 V/cm')
    make_band_plot(20)
    print('Making band plot, 200 V/cm')
    make_band_plot(200)