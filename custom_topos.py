from mininet.topo import Topo

class BaselineTopo(Topo):
    "Single host connected to 2 clients via 1 switch each."
    def build(self):
        switch1 = self.addSwitch('s1')

        server = self.addHost('server')
        self.addLink(server, switch1)
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
        switch = self.addSwitch('s1')
        server = self.addHost('server')
        self.addLink(server, switch)
        command = self.addHost('command')
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
