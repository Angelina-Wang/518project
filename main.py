#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from custom_classes import *
import ipdb

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
        server = self.addHost('server', cls=HostServer)
        self.addLink(server, switch1)
        #self.addLink(server, switch2)

        #client1 = self.addHost('client1', cls=HostWithTime)
        #client2 = self.addHost('client2', cls=HostWithTime)
        client1 = self.addHost('client1', cls=HostClient)
        client2 = self.addHost('client2', cls=HostClient)
        self.addLink(client1, switch1, bw=10, delay='5ms')
        self.addLink(client2, switch1, bw=20, delay='10ms')

def simpleTest():
    "Create and test a simple network"
    topo = BaselineTopo()
    net = Mininet(topo, link=TCLink)
    net.start()
    client1, client2, server = net.get('client1', 'client2', 'server')
    client1.connectServer(server.IP())
    client1.sendToServer('hello')
    ipdb.set_trace()
    # server.restart(100)
    # print 'here is the time now'
    # print server.getTime()
    # print "Dumping host connections"
    # dumpNodeConnections(net.hosts)
    # print "Testing network connectivity"
    # net.pingAll()
    # print "Testing bandiwdth"

    # print 'here is the time at the end'
    # print server.getTime()

    #net.iperf( (client1, server) )
    #net.iperf( (client2, server) )
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
