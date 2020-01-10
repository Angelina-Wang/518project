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
        times = [chunk[num] for chunk in arr][:10]
        trials.append(np.mean(times))
        print('Client {0}: {1}+-{2}'.format(num, np.mean(times), np.std(times)))
    print("Overall: {0} +- {1} of {2} trials".format(np.mean(trials), np.std(trials), num_trials))
elif hps.f[:9] == 'hierarchy':
    arr = pkl.load(open(hps.f, 'rb'))
    num_clients = len(arr[0])
    num_trials = len(arr)
    trials = []
    for num in range(num_clients):
        times = [chunk[num] for chunk in arr][:10]
        print('Client {0}: {1}+-{2}'.format(num, np.mean(times), np.std(times)))
elif hps.f == 'dynamic':
    join = pkl.load(open('dynamic_join', 'rb'))
    leave = pkl.load(open('dynamic_leave', 'rb'))
    base = [x[:3] for x in join]
    base.extend([x[:-3] for x in leave])
    join = [x[3:] for x in join]
    leave = [x[3:] for x in leave]

    flatten = lambda l: [item for sublist in l for item in sublist]
    join = flatten(join)
    base = flatten(base)
    leave = flatten(leave)

    print('base: {0} +- {1}'.format(np.mean(base), np.std(base)))
    print('join: {0} +- {1}'.format(np.mean(join), np.std(join)))
    print('leave: {0} +- {1}'.format(np.mean(leave), np.std(join)))
    
else:
    print hps.f
    arr = pkl.load(open(hps.f, 'rb'))
    print np.mean(arr)
    print np.std(arr)
