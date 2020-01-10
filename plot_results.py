import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import pickle
import numpy as np

def something():
    a = 1
def multiple():
    means = []
    stds = []
    x = []
    #for i in range(1, 11):
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
    parse.add_argument('--version', type=int, default=0)
    hps = parse.parse_args()
    if hps.version == 0:
        something()
    elif hps.version == 1:
        multiple()
    elif hps.version == 2:
        hierarchy()
    elif hps.version == 3:
        sendLots()

