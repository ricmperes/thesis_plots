import numpy as np
import matplotlib.pyplot as plt
import json
from tqdm import tqdm

from pylars.plotting import *


def plot_wf_PEs(figax = None):
    """Plot waveforms of 1, 2 and 3 PEs from a quad.
    
    The datasets of origin is run6, 170K, 52 V, LED OFF data, module 0, 
    channel 'wf0'. WF numbers:
        * 1pe: 99545
        * 2pe: 48037
        * 3pe: 38193
    """
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (8,2), dpi = 100)
    else:
        fig, ax = figax

    with open('./Data/waveform_123pe.json', 'r') as json_file:
        wf_dict = json.load(json_file)

    pos_pe1 = wf_dict['1']['pos']
    pos_pe2 = wf_dict['2']['pos']
    pos_pe3 = wf_dict['3']['pos']
    length_pe1 = wf_dict['1']['length']
    wfpe1 = wf_dict['1']['data']
    wfpe2 = wf_dict['2']['data']
    wfpe3 = wf_dict['3']['data']

    ax.plot(np.arange(pos_pe1-200,pos_pe1 + length_pe1 + 200), 
            wfpe1[pos_pe1-200:pos_pe1 + length_pe1 + 200],
        alpha = 1, label = '1 pe', zorder = 9)

    ax.plot(np.arange(pos_pe1-200,pos_pe1 + length_pe1 + 200), 
            wfpe2[pos_pe2-200:pos_pe2 + length_pe1 + 200],
        alpha = 1, label = '2 pe', zorder = 8)

    ax.plot(np.arange(pos_pe1-200,pos_pe1 + length_pe1 + 200), 
            wfpe3[pos_pe3-200:pos_pe3 + length_pe1 + 200],
        alpha = 1, label = '3 pe', zorder = 7)

    ax.set_xticks(np.arange(pos_pe1-200,pos_pe1 + length_pe1 + 200, 100), 
                  np.arange(-200,201,100))
    ax.set_ylabel('ADC counts')
    ax.set_xlabel('Sample number from pulse')
    ax.legend()
    
    return fig, ax

def plot_wf_LED(figax = None):
    """Plot waveforms of 1, 2 and 3 PEs from a quad.
    
    The datasets of origin is run6, 170K, 52 V, LED ON data, module 0, 
    channel 'wf3'. WF number: 2
    """
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (8,2), dpi = 100)
    else:
        fig, ax = figax

    with open('./Data/waveform_LED.json', 'r') as json_file:
        wf_dict = json.load(json_file)

    pos_LED = wf_dict['pos']
    length_LED = wf_dict['length']
    wfLED = wf_dict['data']

    ax.plot(np.arange(pos_LED-200,pos_LED + length_LED + 200), 
            wfLED[pos_LED-200:pos_LED + length_LED + 200],
        alpha = 1, label = 'LED pulse', zorder = 9)

    ax.set_xticks(np.arange(pos_LED-200,pos_LED + length_LED + 200, 100), 
                  np.arange(-200,201,100))
    ax.set_ylabel('ADC counts')
    ax.set_xlabel('Sample number from pulse')
    ax.legend()
    
    return fig, ax

def plot_wf_noise(figax = None):
    """Plot waveforms of 1, 2 and 3 PEs from a quad.
    
    The datasets of origin is run6, 170K, 52 V, LED OFF data, module 0, 
    channel 'wf0'. WF number: 2
    """
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (8,2), dpi = 100)
    else:
        fig, ax = figax

    with open('./Data/waveform_LED.json', 'r') as json_file:
        wf_dict = json.load(json_file)

    pos_LED = wf_dict['pos']
    length_LED = wf_dict['length']
    wfLED = wf_dict['data']

    ax.plot(np.arange(pos_LED-200,pos_LED + length_LED + 200), 
            wfLED[pos_LED-200:pos_LED + length_LED + 200],
        alpha = 1, label = 'LED pulse', zorder = 9)

    ax.set_xticks(np.arange(pos_LED-200,pos_LED + length_LED + 200, 100), 
                  np.arange(-200,201,100))
    ax.set_ylabel('ADC counts')
    ax.set_xlabel('Sample number from pulse')
    ax.legend()
    
    return fig, ax
    
def plot_wf_LED_stacked(n_waveforms = 200, LED_pos = 300, figax = None):
    if figax == None:
        fig, ax = plt.subplots(1,1, figsize = (8,2), dpi = 100)
    else:
        fig, ax = figax

    if n_waveforms > 500:
        raise AttributeError('Only 500 waveforms available on the file cut.')
    ch = np.load('./Data/LED_array_500_wfs.npy')

    for i in tqdm(range(n_waveforms)):
        ax.plot(np.arange(LED_pos-200,LED_pos+300), 
                            ch[i][LED_pos-200:LED_pos+300], 
                alpha = 0.1, 
                c = plt.rcParams['axes.prop_cycle'].by_key()['color'][0])
    
    ax.set_ylabel('ADC counts')
    ax.set_xlabel('Sample number from pulse')

    return fig, ax
        