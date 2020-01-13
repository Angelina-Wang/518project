#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
import pdb
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP
from scapy.sendrecv import send
from scapy.all import *
import asyncore
import threading
import itertools
from threading import Thread
from argparse import ArgumentParser
import numpy as np
import subprocess
import os
import pickle as pkl
from mininet.node import CPULimitedHost
from custom_classes import *
from custom_tests import *
from custom_topos import *
from utils import *

def parse_args():
    parser = ArgumentParser()

    parser.add_argument('--delay', default=5, type=int,
                        help='changes the delay to client 2')
    parser.add_argument('--depth', default=2, type=int,
                        help='depth of hierarchy')
    parser.add_argument('--bw', default=1.0, type=float,
                        help='changes bandwidth of link to client 2')
    parser.add_argument('--version', default=0, type=int,
                        help='which version of test to run')
    parser.add_argument('--num_clients', default=2, type=int,
                        help='number of clients')
    parser.add_argument('--num_trials', default=1, type=int,
                        help='number of trials for variance testing')
    parser.add_argument('--cpu_frac', default=0.01, type=float,
                        help='percent of CPU to give to the server in cpu-limiting test')

    return parser.parse_args()

if __name__ == '__main__':
    setLogLevel('info')

    hps = parse_args()

    if hps.version == 0:
        variableDelayBWTest(hps)
    elif hps.version == 1:
        multiClientTest(hps)
    elif hps.version == 2:
        busyClientTest(hps)
    elif hps.version == 3:
        sendLotsTest()
    elif hps.version == 4:
        hierarchyTest(hps)
    elif hps.version == 5:
        dynamicTest(hps)

