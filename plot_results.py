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
    plt.savefig('multiple.png')
        

if __name__ == '__main__':
    parse = ArgumentParser()
    parse.add_argument('--version', type=int, default=0)
    hps = parse.parse_args()
    if hps.version == 0:
        something()
    if hps.version == 1:
        multiple()
