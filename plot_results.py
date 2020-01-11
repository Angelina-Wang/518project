import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import pickle
import numpy as np
import glob

def busy():
    c2_means = []
    c2_stds = []

    x = [0.001, 0.01, 0.1, 0.25, 0.3]
    for i in x:
        c2_arr = pickle.load(open('busy{}_c2'.format(i), 'rb'))
        c2_means.append(np.mean(c2_arr))
        c2_stds.append(np.std(c2_arr))

    plt.errorbar(x, c2_means, c2_stds, label='variable delay')

    plt.xlabel('Percentage of CPU granted to server')
    plt.ylabel('Time difference from server (s)')

    plt.title('Available Compute vs Time Difference')
    plt.xlim([-0.01, 0.5])
    plt.savefig('busy_plot.png')

def delay():
    bases = []
    c2_means = []
    c2_stds = []
    x = np.arange(1, 10)

    for i in x:
        c1_arr = pickle.load(open('c1_d{}'.format(i), 'rb'))
        c2_arr = pickle.load(open('c2_d{}'.format(i), 'rb'))
        bases.extend(c1_arr)
        c2_means.append(np.mean(c2_arr))
        c2_stds.append(np.std(c2_arr))

    plt.errorbar(x, c2_means, c2_stds, label='variable delay')

    plt.xlabel('Delay (ms)')
    plt.ylabel('Time Difference from Server (s)')

    plt.title('Delay vs Time Difference')
    plt.xlim([0, 11])
    plt.savefig('delay_plot.png')
    
def bw():
    bases = []
    c2_means = []
    c2_stds = []
    x = [0.001, 0.01, 0.1, 1.0, 10.0]

    for i in x:
        c1_arr = pickle.load(open('c1_bw{}'.format(i), 'rb'))
        c2_arr = pickle.load(open('c2_bw{}'.format(i), 'rb'))
        bases.extend(c1_arr)
        c2_means.append(np.mean(c2_arr))
        c2_stds.append(np.std(c2_arr))

    base_mean = np.mean(bases)
    base_std = np.std(bases)
    plt.errorbar(x, c2_means, yerr=c2_stds, label='variable bw')

    plt.xlabel('Bandwidth (Mbit/s)')
    plt.ylabel('Time Difference from Server (s)')
    plt.xscale('log')
    plt.title('Bandwidth vs Time Difference')
    plt.xlim([0, 11])
    plt.savefig('bw_plot.png')

def multiple():
    means = []
    stds = []
    x = []
    for i in [2, 4, 6, 8, 10]:
        arr = pickle.load(open('multiple_{}'.format(i), 'rb'))
        num_clients = len(arr[0])
        trials = []
        for num in range(num_clients):
            times = [chunk[num] for chunk in arr][:10]
            trials.append(np.mean(times))
        means.append(np.mean(trials))
        stds.append(np.std(trials))
        x.append(i)
    plt.errorbar(x, means, yerr=stds)
    plt.xlabel('Number of Clients')
    plt.ylabel('Drift from Server (s)')
    plt.title('Multiple Clients')
    plt.xlim([0, 11])
    plt.savefig('multiple.png')

def hierarchy():
    for i in [2, 4, 6, 8, 10]:
        arr = pickle.load(open('hierarchy_{}'.format(i), 'rb'))
        num_clients = len(arr[0])
        means = []
        stds = []
        x = []
        for num in range(num_clients):
            times = [chunk[num] for chunk in arr][:10]
            means.append(np.mean(times))
            stds.append(np.std(times))
            x.append(num+1)
        plt.errorbar(x, means, yerr=stds)
        plt.xlabel('Depth of Hierarchy')
        plt.ylabel('Drift from Server (s)')
        plt.title('{}-Layer Hierarchy'.format(i))
        plt.xlim([0, 11])
        plt.savefig('hierarchy_{}.png'.format(i))
        plt.close()

def sendLots():
    arr = pickle.load(open('sendLots', 'rb'))
    means = []
    stds = []
    for num in range(2):
        times = [chunk[num] for chunk in arr][:10]
        means.append(np.mean(times))
        stds.append(np.std(times))
    tick_label=['Control', 'Busy Link']
    plt.bar([0, 1], means, yerr=stds, alpha=.2)
    plt.xticks([0, 1], tick_label)
    plt.ylabel('Drift from Server (s)')
    plt.title('Congested Links')
    plt.savefig('sendLots.png')

if __name__ == '__main__':
    parse = ArgumentParser()
    parse.add_argument('--test', type=str, default='delay')
    hps = parse.parse_args()
    
    if hps.test == 'delay':
        delay()
    elif hps.test == 'bw':
        bw()
    elif hps.test == 'busy':
        busy()
    elif hps.test == 'multiple':
        multiple()
    elif hps.version == 'hierarchy':
        hierarchy()
    elif hps.version == 'busyPipe':
        sendLots()

