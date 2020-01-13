from mininet.net import Mininet
from mininet.link import TCLink
from scapy.sendrecv import send
from scapy.all import *
from threading import Thread
import numpy as np
import subprocess
import os
import pickle as pkl
from custom_classes import *
from custom_tests import *
from custom_topos import *
from utils import *

# sending lots of things along each link
def sendLotsTest():
    topo = BaselineTopo()
    net = Mininet(topo, link=TCLink)
    net.start()
    client1, client2, server, command = net.get('client1', 'client2', 'server', 'command')
    net.pingAll()
    server.cmd('nohup python -u startServer.py > server_log.txt &')
    off = np.random.randint(0, 50)
    client1.cmd('nohup python -u startClient.py {0} {1} > client1_log.txt  &'.format(server.IP(), off))
    off = np.random.randint(0, 50)
    output = client2.cmd('nohup python -u startClient.py {0} {1} > client2_log.txt &'.format(server.IP(), off))
    time.sleep(2)
    
    print(getTimesMultiple(command, server, [client1, client2]))
    lst = (client2, server)
    Thread(target=net.iperf, args=((lst,))).start()

    output = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'startNTP'))
    print("starting ntp 1")
    print(output)

    output = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'startNTP'))
    print("starting ntp 2")
    print(output)

    times_ = getTimesMultiple(command, server, [client1, client2])
    if os.path.isfile('sendLots'):
        times = pkl.load(open('sendLots', 'rb'))
    else:
        times = []

    times.append(times_)

    pkl.dump(times, open('sendLots', 'wb'))
    net.stop()

def multiClientTest(hps):
    num = hps.num_clients
    topo = BigTopo(num)
    net = Mininet(topo, link=TCLink)
    net.start()
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
        output = command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'startNTP'))
        print("starting ntp {}".format(i+1))
        print(output)

    times_ = getTimesMultiple(command, server, clients)
    print(times_)

    if os.path.isfile('multiple_{}'.format(num)):
        times = pkl.load(open('multiple_{}'.format(num), 'rb'))
    else:
        times = []

    times.append(times_)

    pkl.dump(times, open('multiple_{}'.format(num), 'wb'))
    net.stop()


def dynamicTest(hps):
    num = hps.num_clients
    topo = BigTopo(num)
    net = Mininet(topo, link=TCLink)
    net.start()
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
        output = command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'startNTP'))
        print("starting ntp {}".format(i+1))
        print(output)

        time.sleep(2)

    print('second batch of NTP')
    leaving_clients = clients[:3]
    joining_clients = clients[6:]
    for i, client in enumerate(clients[3:6]):
        print(client)
        if len(leaving_clients) != 0:
            j = np.random.choice(leaving_clients, replace=False)
            print("closing client {}".format(j))
            command.cmd('python startCommander.py {0} {1} &'.format(j.IP(), 'close'))
            leaving_clients.remove(j)

            print("starting ntp {}".format(client))
            output2 = command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'startNTP'))

    times_ = getTimesMultiple(command, server, clients[:6])
    print(times_)

    if os.path.isfile('dynamic_leave'):
        times = pkl.load(open('dynamic_leave', 'rb'))
    else:
        times = []

    times.append(times_)

    pkl.dump(times, open('dynamic_leave', 'wb'))

    for i, client in enumerate(clients[3:6]):
        print(client)
        if len(joining_clients) != 0:
            j = np.random.choice(joining_clients, replace=False)
            print("joining client {}".format(j))
            off = np.random.randint(0, 50)
            j.cmd('nohup python -u startClient.py {0} {1} &'.format(server.IP(), off))
            print("starting ntp {}".format(client))
            output2 = command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'startNTP'))
            joining_clients.remove(j)
            time.sleep(2)

    times_ = getTimesMultiple(command, server, clients[:6])
    print(times_)

    if os.path.isfile('dynamic_join'):
        times = pkl.load(open('dynamic_join', 'rb'))
    else:
        times = []

    times.append(times_)

    pkl.dump(times, open('dynamic_join', 'wb'))

def hierarchyTest(hps):
    "Create and test a simple network"
    num = hps.depth
    topo = HierarchyTopo(hps)
    net = Mininet(topo, link=TCLink)
    net.start()
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

        output = command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'startNTP'))
        print("starting ntp {}".format(i+1))
        print(output)

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
    client1, client2, server, command = net.get('client1', 'client2', 'server', 'command')
    print server.IP()
    print client1.IP()
    net.pingAll()
    output = server.cmd('nohup python -u startServer.py > server_log.txt &')
    print(output)
    output = client1.cmd('nohup python -u startClient.py {0} {1} > client1_log.txt  &'.format(server.IP(), 97))
    print(output)
    output = client2.cmd('nohup python -u startClient.py {0} {1} > client2_log.txt &'.format(server.IP(), 0))
    print(output)
    time.sleep(2)
    
    output = command.cmd('python startCommander.py {0} {1}'.format(server.IP(), 'getTime'))
    print("get time SERVER")
    print(output)
    
    output = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'getTime'))
    print("get time client 1")
    print(output)
    
    output = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'getTime'))
    print("get time client 2")
    print(output)

    output = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'startNTP'))
    print("starting ntp 1")
    print(output)

    output = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'startNTP'))
    print("starting ntp 2")
    print(output)

    a, b = getTimesMultiple(command, server, [client1, client2])
    print('client1 diff')
    print(a)
    print('client2 diff')
    print(b)
   
    net.stop()

def variableDelayBWTest(hps):
    topo = DelayBWTopo(hps)
    
    net = Mininet(topo, link=TCLink)
    net.start()

    client1, client2, server, command = net.get('client1', 'client2', 'server', 'command')
    net.pingAll()

    print('initializing server and clients')
    output1 = server.cmd('nohup python -u startServer.py > server_log.txt &')
    c1_off = np.random.randint(0, 50)
    c2_off = np.random.randint(0, 50)
    output = client1.cmd('nohup python -u startClient.py {0} {1} > client1_log.txt  &'.format(server.IP(), c1_off))
    time.sleep(1)
    output = client2.cmd('nohup python -u startClient.py {0} {1} > client2_log.txt &'.format(server.IP(), c2_off))

    time.sleep(3)

    print('run NTP on client 1')
    output = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'startNTP'))
    print(output)

    print('run NTP on client 2')
    output = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'startNTP'))
    print(output)

    _c1, _c2 = getTimesMultiple(command, server, [client1, client2])

    print(_c1, _c2)
   
    net.stop()

    # we are testing diff delay
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

def busyClientTest(hps):
    topo = CPULimitedTopo(hps)
    
    net = Mininet(topo, link=TCLink)
    net.start()

    client1, client2, server, command = net.get('client1', 'client2', 'server', 'command')
    print server.IP()
    print client1.IP()
    net.pingAll()

    print('initializing server and clients')
    server.cmd('nohup python -u startServer.py > server_log.txt &')
    c1_off = np.random.randint(0, 50)
    c2_off = np.random.randint(0, 50)
    client1.cmd('nohup python -u startClient.py {0} {1} > client1_log.txt  &'.format(server.IP(), c1_off))
    client2.cmd('nohup python -u startClient.py {0} {1} > client2_log.txt &'.format(server.IP(), c2_off))

    time.sleep(3)

    print('run NTP on client 1')
    output = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'startNTP'))
    print(output)
    a = getTimesMultiple(command, server, [client1])

    server.setCPUFrac(hps.cpu_frac)
    output = server.cmd('nohup python -u simulateLoad.py {0} > client2sim_log.txt &'.format(100000))

    print('run NTP on client 2')
    output = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'startNTP'))
    print(output)

    b = getTimesMultiple(command, server, [client2])

    if os.path.isfile('busy{}_c1'.format(hps.cpu_frac)):
        c1 = pkl.load(open('busy{}_c1'.format(hps.cpu_frac), 'rb'))
    else:
        c1 = []

    if os.path.isfile('busy{}_c2'.format(hps.cpu_frac)):
        c2 = pkl.load(open('busy{}_c2'.format(hps.cpu_frac), 'rb'))
    else:
        c2 = []

    c1.append(a)
    c2.append(b)

    pkl.dump(c1, open('busy{}_c1'.format(hps.cpu_frac), 'wb'))
    pkl.dump(c2, open('busy{}_c2'.format(hps.cpu_frac), 'wb'))
   
    net.stop()
