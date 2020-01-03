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
        client1 = self.addHost('client1', cls=HostClient)
        client2 = self.addHost('client2', cls=HostClient)
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
    output = client1.cmd('python startClient.py &')
    print(output)
    time.sleep(2)
    output2 = command.cmd('python startCommander1.py')
    print("get time")
    print(output2)
    output2 = command.cmd('python startCommander2.py')
    print("starting ntp")
    print(output2)
    #loop_thread = threading.Thread(target=asyncore.loop)
    #loop_thread.start()
    #client1.connectServer(server.IP())
    #client1.connectServer('10.0.0.18')
    #client1.sendToServer('hello')
    #output = client1.cmd('python bg_clock_2.py')
    #print(output)

    # print 'here is the time at the end'
    # print server.getTime()

    #net.iperf( (client1, server) )
    #net.iperf( (client2, server) )
    net.stop()

def rec_func(pkt):
    if hasattr(pkt[IP], 'msg'):
        print('########### RECEIVED ############')
        print(pkt.show())
        print(pkt[IP].msg)
        print('###########')
    print(pkt.show())

def testClock():
    topo = BaselineTopoSysTime()
    net = Mininet(topo, link=TCLink)
    net.start()
    client1, client2, server = net.get('client1', 'client2', 'server')

    client1.cmd('python bg_clock.py &')

    client2.cmd('python bg_clock.py &')
    server.cmd('python bg_clock.py &')

    pkt = IP(dst=client1.IP())/ TCP()
    pkt[IP].msg = 'here'

    sniff(prn=rec_func,filter='ip host %s' % client1.IP(),  store=1) # filter='ip host %s' % client1.IP(), 

    print('########### SENT ###########')
    print(pkt.show())
    print('#############')

    #net.iperf( (client1, server) )
    #net.iperf( (client2, server) )
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
    # testClock()
