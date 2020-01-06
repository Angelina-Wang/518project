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

        #server = self.addHost('server', cls=HostWithTime)
        server = self.addHost('server')
        self.addLink(server, switch1)
        #self.addLink(server, switch2)
        command = self.addHost('command')
        self.addLink(command, switch1)

        #client1 = self.addHost('client1', cls=HostWithTime)
        #client2 = self.addHost('client2', cls=HostWithTime)
        client1 = self.addHost('client1')
        client2 = self.addHost('client2')
        self.addLink(client1, switch1, bw=10, delay='5ms')
        self.addLink(client2, switch1, bw=20, delay='10ms')

class BaselineTopoSysTime(Topo):
    "Single host connected to 2 clients via 1 switch each."
    def build(self):
        switch1 = self.addSwitch('s1')
        # switch2 = self.addSwitch('s2')

        #server = self.addHost('server', cls=HostWithTime)
        server = self.addHost('server')
        self.addLink(server, switch1)
        #self.addLink(server, switch2)

        #client1 = self.addHost('client1', cls=HostWithTime)
        #client2 = self.addHost('client2', cls=HostWithTime)
        client1 = self.addHost('client1')
        client2 = self.addHost('client2')
        self.addLink(client1, switch1, bw=10, delay='5ms')
        self.addLink(client2, switch1, bw=20, delay='10ms')

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
    #asyncore.loop()
    #pdb.set_trace()
    # server.restart(100)
    # print 'here is the time now'
    # print server.getTime()
    # print "Dumping host connections"
    # dumpNodeConnections(net.hosts)
    # print "Testing network connectivity"
    net.pingAll()
    # print "Testing bandiwdth"
    output1 = server.cmd('python startServer.py &')
    print(output1)
    output = client1.cmd('python startClient.py {0} {1} &'.format(server.IP(), 97))
    print(output)
    output = client2.cmd('python startClient.py {0} {1} &'.format(server.IP(), 0))
    print(output)
    time.sleep(2)
    
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

    output2 = command.cmd('python startCommander.py {0} {1}'.format(client1.IP(), 'getTime'))
    print("get time client 1")
    print(output2)
    
    output2 = command.cmd('python startCommander.py {0} {1}'.format(client2.IP(), 'getTime'))
    print("get time client 2")
    print(output2)
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
    # testClock()
