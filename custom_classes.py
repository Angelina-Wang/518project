from mininet.node import Host
import time
import socket
import asyncore
import threading
import pdb

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

class AServer():
	def __init__(self):
		self.start = 0
		self.start_from_epoch = time.time()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind(('0.0.0.0', 12345))
                self.sock.listen(1)
                self.startAccepting()

        def startAccepting(self):
                while True:
                    c, addr = self.sock.accept()
                    if c is not None:
                        while True:
                            msg = c.recv(4096)
                            if 'time' in msg:
                                c.send("I am a server here is the time")
                            elif 'hello' in msg:
                                c.send('heyo there')
                            else:
                                c.send("gimme a better message")

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
