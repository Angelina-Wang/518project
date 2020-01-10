import pickle as pkl
import numpy as np
from argparse import ArgumentParser

parse = ArgumentParser()
parse.add_argument('-f', type=str, default=None)
hps = parse.parse_args()

assert hps.f is not None
print("------------{}-------------".format(hps.f))
if hps.f[:8] == 'multiple':
    arr = pkl.load(open(hps.f, 'rb'))
    num_clients = len(arr[0])
    num_trials = len(arr)
    trials = []
    for num in range(num_clients):
        times = [chunk[num] for chunk in arr]
        trials.append(np.mean(times))
        print('Client {0}: {1}+-{2}'.format(num, np.mean(times), np.std(times)))
    print("Overall: {0} +- {1} of {2} trials".format(np.mean(trials), np.std(trials), len(trials)))
else:
    print hps.f
    arr = pkl.load(open(hps.f, 'rb'))
    print np.mean(arr)
    print np.std(arr)
