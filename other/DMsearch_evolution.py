import matplotlib.pyplot as plt
import numpy as np

def load_data():
    argon = np.loadtxt('cross_section_evolution/argon.csv', delimiter=',')
    xenon = np.loadtxt('cross_section_evolution/xenon.csv', delimiter=',')
    bubble = np.loadtxt('cross_section_evolution/bubble.csv', delimiter=',')
    crystals = np.loadtxt('cross_section_evolution/crystals.csv', delimiter=',')
    cryogenic = np.loadtxt('cross_section_evolution/cryogenic.csv', delimiter=',')

    data = {'crystals': crystals,
            'cryogenic': cryogenic,
            'bubble': bubble,
            'argon': argon,
            'xenon': xenon}
    
    return data

def make_plot(data):
    plt.figure(figsize=(4, 3))
    plt.xlabel('Year')
    plt.ylabel('DM-nucleon cross section\n@50 GeV [cm$^2$]')
    plt.xlim(1985, 2025)
    plt.ylim(5e-48, 9e-39)
    plt.yscale('log')

    markers = ['o', 's', 'D', 'v', '^']
    for i,key in enumerate(data.keys()):
        if len(np.shape(data[key])) >1:
            plt.plot(data[key][:, 0], data[key][:, 1], label=key, 
                    ls = '', marker = markers[i])
        else:
            plt.plot(data[key][0], data[key][1], label=key, 
                    ls = '', marker = markers[i])

    plt.legend(loc='upper right')
    plt.savefig('cross_section_evolution/cross_section_evolution.pdf')
    plt.savefig('cross_section_evolution/cross_section_evolution.png')        
    return None

if __name__ == '__main__':
    plt.style.use('../thesis_style.mplstyle')
    data = load_data()
    make_plot(data)
