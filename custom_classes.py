from mininet.node import Host
import time
import socket
import asyncore
import pdb
from threading import Thread

class AServer():
    def __init__(self, n=2):
        self.start = 0
        self.start_from_epoch = time.time()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', 12345))
        self.sock.listen(n)
        self.n = n
        self.startAccepting()

    def connectNew(self, client, addr):
        print('connecting ', addr)
        while True:
            msg = client.recv(4096)
            part1 = self.getTime()
            if 'startNTP' in msg:
                client.send(str(part1) + '|' + str(self.getTime()))
            elif 'getTime' in msg:
                client.send(str(self.getTime()))
            elif 'close' in msg:
                clients.remove(client)
                addrs.remove(addr)
                client.close()
                break 
        return

    def startAccepting(self):
        clients = []
        addrs = []
        
        while True:
            c, addr = self.sock.accept()
            if c is not None:
                clients.append(c)
                addrs.append(addr)
                Thread(target=self.connectNew, args=(c, addr)).start()
                

    def restart(self, start):
        self.start = start
        self.start_from_epoch = time.time()

    def getTime(self):
        return time.time() - self.start_from_epoch + self.start
class AClient():
    def __init__(self):
        self.start = 0
        self.start_from_epoch = time.time()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def startListener(self):
        self.commandSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commandSock.bind(('0.0.0.0', 12345))
        self.commandSock.listen(100)
        self.startAccepting()

    def connectNew(self, c, addr):
        print('connecting ', addr)
        while True:
            msg = c.recv(4096)
            part1 = self.getTime()
            if 'startNTP' in msg:

                t_0 = self.getTime()
                response = self.sendToServer('startNTP').split('|')
                t_3 = self.getTime()
                t_1, t_2 = float(response[0]), float(response[1])
                offset = ((t_1 - t_0) + (t_2-t_3)) / 2.
                self.restart(self.getTime()+offset)
                c.send(str(part1) + '|' + str(self.getTime()))
            elif 'getTime' in msg:
                c.send(str(self.getTime()))
            elif 'close' in msg:
                clients.remove(c)
                addrs.remove(addr)
                c.close()
                break 
        return

    def startAccepting(self):
        clients = []
        addrs = []
        
        while True:
            c, addr = self.commandSock.accept()
            if c is not None:
                clients.append(c)
                addrs.append(addr)
                Thread(target=self.connectNew, args=(c, addr)).start()          

    def connectServer(self, addr, port=12345):
        self.sock.connect((addr, port))

    def sendToServer(self, msg):
        self.sock.send(msg)
        return self.sock.recv(4096)

    def restart(self, start):
        self.start = start
        self.start_from_epoch = time.time()

    def getTime(self):
        return time.time() - self.start_from_epoch + self.start
    
    def close(self):
        self.sock.close()
