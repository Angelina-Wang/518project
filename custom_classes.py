from mininet.node import Host
import time
import socket
import asyncore
import threading
import pdb
import thread
from threading import Thread

class EchoHandlerServer(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)
        pdb.set_trace()
        if data:
            print("I am a server")
            self.send('I am a server')

class EchoHandlerClient(asyncore.dispatcher_with_send):
    def writable(self):
        return 0
    def handle_connect(self):
        print("CONNECTING?")
        pdb.set_trace()
    def handle_read(self):
        pdb.set_trace()
        data = self.recv(8192)
        if data:
            print("I am a client")
            self.send('I am a client')
    def handle_expt(self):
        self.close()


class EchoServer(asyncore.dispatcher):
    def __init__(self, port=12345):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('0.0.0.0', port))
        #self.bind(('127.0.0.1', port))
        self.listen(5)

    def handleAccept(self):
        pdb.set_trace()
        pair = self.accept()
        if pair is not None:
            c, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandlerServer(c)

class EchoClient(asyncore.dispatcher):
    def __init__(self, host, port=12345):
                #pdb.set_trace()
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        handler = EchoHandlerClient(self)

class HostServer(Host):
    def __init__(self, name, inNamespace=True, **params):
        super(HostServer, self).__init__(name, inNamespace, **params)
        self.start = 0
        self.start_from_epoch = time.time()
        self.server = EchoServer()
                #self.thread = threading.Thread(target=asyncore.loop, kwargs={'timeout':1})
                #self.thread.start()
        #asyncore.loop()
                #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.sock.bind(('0.0.0.0', 12345))

    def restart(self, start):
        self.start = start
        self.start_from_epoch = time.time()

    def getTime(self):
        return time.time() - self.start_from_epoch + self.start

class HostClient(Host):
    def __init__(self, name, inNamespace=True, **params):
        super(HostClient, self).__init__(name, inNamespace, **params)
        self.start = 0
        self.start_from_epoch = time.time()
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectServer(self, addr, port=12345):
                #self.thread = threading.Thread(target=asyncore.loop, kwargs={'timeout':1})
                #self.thread.start()
        self.client = EchoClient(addr, port)
        # self.sock.connect((addr, port))
        # handler = EchoHandlerClient(self.sock)
        # asyncore.loop()

    def sendToServer(self, msg):
                pdb.set_trace()
                self.client.send(msg)
        #self.sock.send(msg)

    def restart(self, start):
        self.start = start
        self.start_from_epoch = time.time()

    def getTime(self):
        return time.time() - self.start_from_epoch + self.start

#class CommandServer():
#   def __init__(self):
#       self.start = 0
#       self.start_from_epoch = time.time()
#       self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                self.sock.bind(('0.0.0.0', 12345))
#                self.sock.listen(1)
#                self.startAccepting()
#
#        def startAccepting(self):
#                while True:
#                    c, addr = self.sock.accept()
#                    if c is not None:
#                        msg = c.recv(4096)
#                        if 'askTime' in msg:
#                            c.send("time")
#                        elif 'hello' in msg:
#                            c.send('heyo there')
#                        else:
#                            c.send("gimme a better message")
#                        c.close()
#
#   def restart(self, start):
#       self.start = start
#       self.start_from_epoch = time.time()
#
#   def getTime(self):
#       return time.time() - self.start_from_epoch + self.start
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
            client.send('connected')
            part1 = self.getTime()
            if 'startNTP' in msg:
                client.send(str(part1) + '|' + str(self.getTime()))

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
                #thread.start_new_thread(connectNew, (c, addr))
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

    def startAccepting(self):
        while True:
            c, addr = self.commandSock.accept()
            if c is not None:
                msg = c.recv(4096)
                if 'startNTP' in msg:

                    t_0 = self.getTime()
                    response = self.sendToServer('startNTP').split('|')
                    c.send(response)
                    """

                    t_3 = self.getTime()
                    t_1, t_2 = float(response[0]), float(response[1])
                    offset = ((t_1 - t_0) + (t_2-t_3)) / 2.


                    offset = 5
                    self.restart(self.start+offset)
                    c.send(str(offset))
                    """
                elif 'getTime' in msg:
                    c.send(str(self.getTime()))
                else:
                    c.send('back at ya')
                c.close()

    def connectServer(self, addr, port=12345):
        #self.thread = threading.Thread(target=asyncore.loop, kwargs={'timeout':1})
        #self.thread.start()
        self.sock.connect((addr, port))
        # handler = EchoHandlerClient(self.sock)
        # asyncore.loop()

    def sendToServer(self, msg):
        self.sock.send(msg)
        return self.sock.recv(4096)
        #self.sock.send(msg)

    def restart(self, start):
        self.start = start
        self.start_from_epoch = time.time()

    def getTime(self):
        return time.time() - self.start_from_epoch + self.start
    
    def close(self):
        self.sock.close()
