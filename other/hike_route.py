import matplotlib.pyplot as plt
import numpy as np

plt.style.use('../thesis_style.mplstyle')

def load_data():
    part1 = np.loadtxt('via_alpina_no1/part1.csv', delimiter=',')
    part2 = np.loadtxt('via_alpina_no1/part2.csv', delimiter=',')
    part3 = np.loadtxt('via_alpina_no1/part3.csv', delimiter=',')
    part4 = np.loadtxt('via_alpina_no1/part4.csv', delimiter=',')
    route = np.vstack((part1, part2, part3, part4))
    return route

def plot_route(data, figax = None):
    if figax is None:
        fig, ax = plt.subplots(figsize=(16/2,9/3))
    else:
        fig, ax = figax
    
    ax.plot(data[:,0], data[:,1])
    ax.set_xticks(np.linspace(0,365, 5),
                  list(np.arange(0, 1, 0.25))+[0.99])
    ax.set_xlabel('PhD completeness')
    ax.set_yticks([],[])#ax.set_yabel('')
    if figax is None:
        fig.savefig('route.pdf')
        fig.savefig('route.png')
        plt.close()
    else:
        return fig, ax    

def get_peaks(data):
    peaks_x = []
    peaks_y = []
    for i in range(1, len(data) - 1):
        if data[i,1] > data[i-1,1] and data[i,1] > data[i+1,1]:
            peaks_x.append(data[i,0])
            peaks_y.append(data[i,1])
    return np.array([peaks_x, peaks_y]).T

def plot_peaks(peaks, figax = None):
    if figax is None:
        fig, ax = plt.subplots(figsize=(16/2,9/3))
    else:
        fig, ax = figax
    labels = np.loadtxt('milestones.csv', delimiter=',', dtype=str)
    for i in range(len(peaks)):
        ax.plot([peaks[i,0],peaks[i,0]], [0,peaks[i,1]], 
                   color='k', alpha=0.5, ls = '--')
        ax.text(peaks[i,0] - 2, peaks[i,1] + 120, str(labels[i]), fontsize = 8,
                rotation = -290)
    return fig, ax

if __name__ == '__main__':
    data = load_data()
    #peaks = get_peaks(data)
    #np.savetxt('peaks.csv', peaks, delimiter=',')
    #plot_route(data)
    peaks = np.loadtxt('peaks_select.csv', delimiter=',')
    fig, ax = plt.subplots(figsize=(16/2,9/3))
    fig, ax = plot_route(data, figax = (fig, ax))
    fig, ax = plot_peaks(peaks, figax = (fig, ax))
    #ax.set_xlabel('')
    #ax.set_ylabel('')
    ax.set_ylim(-1,4500)
    #ax.set_xlim(0,400)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    fig.savefig('route_peaks.pdf')
    fig.savefig('route_peaks.png')
