import pickle as pkl
import numpy as np
from argparse import ArgumentParser

parse = ArgumentParser()
parse.add_argument('-f', type=str, default=None)
hps = parse.parse_args()

assert hps.f is not None

print hps.f
arr = pkl.load(open(hps.f, 'rb'))
print np.mean(arr)
print np.std(arr)
