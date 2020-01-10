import matplotlib.pyplot as plt
from argparse import ArgumentParser

def something():
    a = 1

if __name__ == '__main__':
    parse = ArgumentParser()
    parse.add_argument('--version', type=int, default=0)
    hps = parse.parse_args()
    if hps.version == 0:
        something()
    if hps.version == 1:
        j
