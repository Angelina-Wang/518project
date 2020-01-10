#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from custom_classes import *
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

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)

class BaselineTopo(Topo):
    "Single host connected to 2 clients via 1 switch each."
    def build(self):
        switch1 = self.addSwitch('s1')
        # switch2 = self.addSwitch('s2')

        server = self.addHost('server')
        self.addLink(server, switch1)
        #self.addLink(server, switch2)
        command = self.addHost('command')
        self.addLink(command, switch1)

        client1 = self.addHost('client1')
        client2 = self.addHost('client2')
        self.addLink(client1, switch1, bw=10, delay='5ms')
        self.addLink(client2, switch1, bw=10, delay='5ms')

class BigTopo(Topo):
    def __init__(self, num):
        self.numClients = num
        super(BigTopo, self).__init__()

    def build(self):
        switch1 = self.addSwitch('s1')
        # switch2 = self.addSwitch('s2')

        server = self.addHost('server')
        self.addLink(server, switch1)
        command = self.addHost('command')
        self.addLink(command, switch1)
        
        clients = []
        for i in range(self.numClients):
            client = self.addHost('client{}'.format(i+1))
            clients.append(client)
        for client in clients:
            self.addLink(client, switch1, bw=1, delay='5ms')

class DelayBWTopo(Topo):
    "Single host connected to 2 clients via 1 switch each."
    def __init__(self, hps):
        self.bw = hps.bw
        self.delay = hps.delay
        super(DelayBWTopo, self).__init__()
        
    def build(self):
        switch1 = self.addSwitch('s1')

        server = self.addHost('server')
        self.addLink(server, switch1)
        command = self.addHost('command')
        self.addLink(command, switch1)

        client1 = self.addHost('client1')
        client2 = self.addHost('client2')
        self.addLink(client1, switch1, bw=1, delay='5ms')
        self.addLink(client2, switch1, bw=self.bw, delay='{}ms'.format(self.delay))

class HierarchyTopo(Topo):
    "Single host connected to 2 clients via 1 switch each."
    def __init__(self, hps):
        self.bw = hps.bw
        self.depth = hps.depth
        super(HierarchyTopo, self).__init__()
        
    def build(self):
        #switches = []
        #for i in range(self.depth):
        #    switch = self.addSwitch('s{}'.format(i+1))
        #    switches.append(switch)
        switch = self.addSwitch('s1')

        server = self.addHost('server')
        #self.addLink(server, switches[0])
        self.addLink(server, switch)
        command = self.addHost('command')
        #self.addLink(command, switches[0])
        self.addLink(command, switch)
        clients = []

        for i in range(self.depth):
            client = self.addHost('client{}'.format(i+1))
            clients.append(client)

        for client in clients:
            self.addLink(client, switch, bw=1, delay='5ms')

class CPULimitedTopo(Topo):
    "Single host connected to 2 clients via 1 switch each."
    def __init__(self, hps):
        self.bw = hps.bw
        self.delay = hps.delay
        super(CPULimitedTopo, self).__init__()
        
    def build(self):
        switch1 = self.addSwitch('s1')

        server = self.addHost('server', cls=CPULimitedHost)
        self.addLink(server, switch1)
        command = self.addHost('command')
        self.addLink(command, switch1)

        client1 = self.addHost('client1')
        client2 = self.addHost('client2', cls=CPULimitedHost)
        self.addLink(client1, switch1, bw=1, delay='5ms')
        self.addLink(client2, switch1, bw=self.bw, delay='{}ms'.format(self.delay))

def getTimesMultiple(command, server, clientList):
    #perms = list(itertools.permutations(clientList))
    #diffs = np.zeros(len(clientList))

    #for perm in perms:
    #    serverTime_ = float(command.cmd('python startCommander.py {0} {1}'.format(server.IP(), 'getTime')))
    #    for client in perm:
    #        clientTime = float(command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'getTime')))
    #        diffs[int(client.name[6:])] += (clientTime - serverTime)
   
    diffs = []
    for client in clientList:
        a = time.time()
        serverTime = float(command.cmd('python startCommander.py {0} {1}'.format(server.IP(), 'getTime')))
        b = time.time()
        clientTime = float(command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'getTime')))
        c = time.time()

        serverAdjust = serverTime + (b-a)/2.
        clientAdjust = clientTime - (c-b)/2.
        
        diffs.append(np.abs(serverAdjust-clientAdjust))

    return diffs

def variableDelayBW(hps):
    topo = DelayBWTopo(hps)
    
    net = Mininet(topo, link=TCLink)
    net.start()

    client1, client2, server, command = net.get('client1', 'client2', 'server', 'command')
    print server.IP()
    print client1.IP()
    net.pingAll()

    print('initializing server and clients')
    output1 = server.cmd('nohup python -u startServer.py > server_log.txt &')
    c1_off = np.random.randint(0, 50)
    c2_off = np.random.randint(0, 50)
    output = client1.cmd('nohup python -u startClient.py {0} {1} > client1_log.txt  &'.format(server.IP(), c1_off))
    output = client2.cmd('nohup python -u startClient.py {0} {1} > client2_log.txt &'.format(server.IP(), c2_off))

    time.sleep(3)

    print('run NTP on client 1')
    output2 = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'startNTP'))
    print(output2)

    print('run NTP on client 2')
    output2 = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'startNTP'))
    print(output2)

    _c1, _c2 = getTimesMultiple(command, server, [client1, client2])

    print(_c1, _c2)
   
    net.stop()

    # we are testing diff delay
    if hps.delay != 5:
        if os.path.isfile('c1_d{}'.format(hps.delay)):
            c1 = pkl.load(open('c1_d{}'.format(hps.delay), 'rb'))
            c2 = pkl.load(open('c2_d{}'.format(hps.delay), 'rb'))
        else:
            c1 = []
            c2 = []

        c1.append(_c1)
        c2.append(_c2)

        pkl.dump(c1, open('c1_d{}'.format(hps.delay), 'wb'))
        pkl.dump(c2, open('c2_d{}'.format(hps.delay), 'wb'))

    # we are testing diff bandwidth
    if hps.bw != 1:
        if os.path.isfile('c1_bw{}'.format(hps.bw)):
            c1 = pkl.load(open('c1_bw{}'.format(hps.bw), 'rb'))
            c2 = pkl.load(open('c2_bw{}'.format(hps.bw), 'rb'))
        else:
            c1 = []
            c2 = []

        c1.append(_c1)
        c2.append(_c2)

        pkl.dump(c1, open('c1_bw{}'.format(hps.bw), 'wb'))
        pkl.dump(c2, open('c2_bw{}'.format(hps.bw), 'wb'))

    return _c1, _c2

def busyClient(hps):
    topo = CPULimitedTopo(hps)
    
    net = Mininet(topo, link=TCLink)
    net.start()

    client1, client2, server, command = net.get('client1', 'client2', 'server', 'command')
    print server.IP()
    print client1.IP()
    net.pingAll()

    print('initializing server and clients')
    output1 = server.cmd('nohup python -u startServer.py > server_log.txt &')
    c1_off = np.random.randint(0, 50)
    c2_off = np.random.randint(0, 50)
    output = client1.cmd('nohup python -u startClient.py {0} {1} > client1_log.txt  &'.format(server.IP(), c1_off))
    output = client2.cmd('nohup python -u startClient.py {0} {1} > client2_log.txt &'.format(server.IP(), c2_off))

    time.sleep(3)

    print('run NTP on client 1')
    output2 = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'startNTP'))
    print(output2)
    a = getTimesMultiple(command, server, [client1])

    server.setCPUFrac(hps.cpu_frac)
    output = server.cmd('nohup python -u simulateLoad.py {0} > client2sim_log.txt &'.format(100000))

    print('run NTP on client 2')
    output2 = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'startNTP'))
    print(output2)

    b = getTimesMultiple(command, server, [client2])
    print('client1 diff')
    print(a)
    print('client2 diff')
    print(b)
   
    net.stop()

# sending lots of things along each link
def sendLotsTest():
    topo = BaselineTopo()
    net = Mininet(topo, link=TCLink)
    net.start()
    client1, client2, server, command = net.get('client1', 'client2', 'server', 'command')
    net.pingAll()
    output1 = server.cmd('nohup python -u startServer.py > server_log.txt &')
    off = np.random.randint(0, 50)
    output = client1.cmd('nohup python -u startClient.py {0} {1} > client1_log.txt  &'.format(server.IP(), off))
    off = np.random.randint(0, 50)
    output = client2.cmd('nohup python -u startClient.py {0} {1} > client2_log.txt &'.format(server.IP(), off))
    time.sleep(2)
    
    print(getTimesMultiple(command, server, [client1, client2]))
    #net.iperf((client1, server))
    lst = (client2, server)
    Thread(target=net.iperf, args=((lst,))).start()
    #Thread(target=net.iperf, args=((client1, server))).start()

    output2 = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'startNTP'))
    print("starting ntp 1")
    print(output2)

    output2 = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'startNTP'))
    print("starting ntp 2")
    print(output2)

    times_ = getTimesMultiple(command, server, [client1, client2])
    if os.path.isfile('sendLots'):
        times = pkl.load(open('sendLots', 'rb'))
    else:
        times = []

    times.append(times_)

    pkl.dump(times, open('sendLots', 'wb'))
    # net.iperf((client2, server))
    net.stop()

def multiClientTest(hps):
    "Create and test a simple network"
    num = hps.num_clients
    topo = BigTopo(num)
    net = Mininet(topo, link=TCLink)
    net.start()
    #asyncore.loop()
    #net.pingAll()
    server, command = net.get('server', 'command')
    server.cmd('nohup python -u startServer.py > server_log.txt &')
    clients = []
    for i in range(num):
        client = net.get('client{}'.format(i+1))
        off = np.random.randint(0, 50)
        client.cmd('nohup python -u startClient.py {0} {1} > client{2}_log.txt  &'.format(server.IP(), off, i))
        clients.append(client)
    time.sleep(2)
   
    times_ = getTimesMultiple(command, server, clients)
    for i, client in enumerate(clients):
        print(client)
        output2 = command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'startNTP'))
        print("starting ntp {}".format(i+1))
        print(output2)

    times_ = getTimesMultiple(command, server, clients)
    print(times_)

    if os.path.isfile('multiple_{}'.format(num)):
        times = pkl.load(open('multiple_{}'.format(num), 'rb'))
    else:
        times = []

    times.append(times_)

    pkl.dump(times, open('multiple_{}'.format(num), 'wb'))
   
    # net.iperf((client1, server))
    # net.iperf((client2, server))
    net.stop()


def dynamicTest(hps):
    num = hps.num_clients
    topo = BigTopo(num)
    net = Mininet(topo, link=TCLink)
    net.start()
    #asyncore.loop()
    #net.pingAll()
    server, command = net.get('server', 'command')
    server.cmd('nohup python -u startServer.py > server_log.txt &')
    clients = []
    for i in range(num):
        client = net.get('client{}'.format(i+1))
        off = np.random.randint(0, 50)
        if i < 6:
            print('starting {}'.format(i))
            client.cmd('nohup python -u startClient.py {0} {1} > client{2}_log.txt  &'.format(server.IP(), off, i))
            time.sleep(1)
        clients.append(client)
    time.sleep(5)
   
    for i, client in enumerate(clients[:3]):
        
        print(client)
        output2 = command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'startNTP'))
        print("starting ntp {}".format(i+1))
        print(output2)

        time.sleep(2)

    print('second batch of NTP')
    leaving_clients = clients[:3]
    joining_clients = clients[6:]
    for i, client in enumerate(clients[3:6]):
        print(client)
        if len(leaving_clients) != 0:
            close_num = np.random.randint(0, len(leaving_clients)//2)
            print("closing {} clients".format(close_num))
            close_ips = np.random.choice(leaving_clients, close_num, replace=False)

            for j in close_ips:
                print("closing client {}".format(j))
                command.cmd('python startCommander.py {0} {1}'.format(j.IP(), 'close'))
                leaving_clients.remove(j)

        if len(joining_clients) != 0:
            join_num = np.random.randint(0, len(joining_clients))
            print("joining {} clients".format(join_num))
            close_ips = np.random.choice(joining_clients, join_num, replace=False)

            for j in close_ips:
                print("joining client {}".format(j))
                off = np.random.randint(0, 50)
                j.cmd('nohup python -u startClient.py {0} {1} &'.format(server.IP(), off))
                joining_clients.remove(j)
                time.sleep(2)

        print("starting ntp {}".format(i+1))
        output2 = command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'startNTP'))
        print(output2)

    if os.path.isfile('multiple_{}'.format(num)):
        times = pkl.load(open('multiple_{}'.format(num), 'rb'))
    else:
        times = []

    times_ = getTimesMultiple(command, server, clients[:6])
    print(times_)
   
    # net.iperf((client1, server))
    # net.iperf((client2, server))

def hierarchyTest(hps):
    "Create and test a simple network"
    num = hps.depth
    topo = HierarchyTopo(hps)
    net = Mininet(topo, link=TCLink)
    net.start()
    #asyncore.loop()
    net.pingAll()
    server, command = net.get('server', 'command')
    clients = []
    server.cmd('nohup python -u startServer.py > server_log.txt &')
    for i in range(num):
        client = net.get('client{}'.format(i+1))
        prev_client = None
        if i != 0:
            prev_client = net.get('client{}'.format(i))
        off = np.random.randint(0, 50)
        if prev_client is None:
            client.cmd('nohup python -u startClient.py {0} {1} > client{2}_log.txt  &'.format(server.IP(), off, i))
        else:
            client.cmd('nohup python -u startClient.py {0} {1} > client{2}_log.txt  &'.format(prev_client.IP(), off, i))
        time.sleep(1)
        clients.append(client)
    time.sleep(2)
   
    times_ = getTimesMultiple(command, server, clients)
    print(times_)
    for i, client in enumerate(clients):

        print(client)
        output2 = command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'startNTP'))
        print("starting ntp {}".format(i+1))
        print(output2)

    times_ = getTimesMultiple(command, server, clients)
    print(times_)

    if os.path.isfile('hierarchy_{}'.format(num)):
        times = pkl.load(open('hierarchy_{}'.format(num), 'rb'))
    else:
        times = []

    times.append(times_)

    pkl.dump(times, open('hierarchy_{}'.format(num), 'wb'))
   
    net.stop()


def simpleTest():
    "Create and test a simple network"
    topo = BaselineTopo()
    net = Mininet(topo, link=TCLink)
    net.start()
    #asyncore.loop()
    client1, client2, server, command = net.get('client1', 'client2', 'server', 'command')
    print server.IP()
    print client1.IP()
    #client1.connectServer(server.IP())
    #client1.connectServer('10.0.0.3')
    #client1.sendToServer('hello')
    # print "Dumping host connections"
    # dumpNodeConnections(net.hosts)
    # print "Testing network connectivity"
    net.pingAll()
    # print "Testing bandiwdth"
    output1 = server.cmd('nohup python -u startServer.py > server_log.txt &')
    print(output1)
    output = client1.cmd('nohup python -u startClient.py {0} {1} > client1_log.txt  &'.format(server.IP(), 97))
    print(output)
    output = client2.cmd('nohup python -u startClient.py {0} {1} > client2_log.txt &'.format(server.IP(), 0))
    print(output)
    time.sleep(2)
    
    output2 = command.cmd('python startCommander.py {0} {1}'.format(server.IP(), 'getTime'))
    print("get time SERVER")
    print(output2)
    
    output2 = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'getTime'))
    print("get time client 1")
    print(output2)
    
    output2 = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'getTime'))
    print("get time client 2")
    print(output2)

    output2 = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'startNTP'))
    print("starting ntp 1")
    print(output2)

    output2 = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'startNTP'))
    print("starting ntp 2")
    print(output2)

    a, b = getTimesMultiple(command, server, [client1, client2])
    print('client1 diff')
    print(a)
    print('client2 diff')
    print(b)
   
    # net.iperf((client1, server))
    # net.iperf((client2, server))
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')

    hps = parse_args()

    if hps.version == 0:
        variableDelayBW(hps)
    elif hps.version == 1:
        multiClientTest(hps)
    elif hps.version == 2:
        busyClient(hps)
    elif hps.version == 3:
        sendLotsTest()
    elif hps.version == 4:
        hierarchyTest(hps)
    elif hps.version == 5:
        dynamicTest(hps)

