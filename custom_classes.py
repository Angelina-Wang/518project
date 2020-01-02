from mininet.node import Host
import time
import socket
import asyncore

class EchoHandlerServer(asyncore.dispatcher_with_send):
	def handle_read(self):
		data = self.recv(8192)
		if data:
			print("I am a server")
			self.send('I am a server')

class EchoHandlerClient(asyncore.dispatcher_with_send):
	def handle_read(self):
		data = self.recv(8192)
		if data:
			print("I am a client")
			self.send('I am a client')

class EchoServer(asyncore.dispatcher):
	def __init__(self, port=12345):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('0.0.0.0', port))
		self.listen(5)

	def handleAccept(self):
		pair = self.accept()
		if pair is not None:
			c, addr = pair
			print 'Incoming connection from %s' % repr(addr)
			handler = EchoHandlerClient(c)

class HostServer(Host):
	def __init__(self, name, inNamespace=True, **params):
		super(HostServer, self).__init__(name, inNamespace, **params)
		self.start = 0
		self.start_from_epoch = time.time()
		self.server = EchoServer()
		asyncore.loop()

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
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connectServer(self, addr, port=12345):
		self.sock.connect((addr, port))
		handler = EchoHandlerClient(self.sock)
		asyncore.loop()

	def sendToServer(self, msg):
		self.sock.send(msg)

	def restart(self, start):
		self.start = start
		self.start_from_epoch = time.time()

	def getTime(self):
		return time.time() - self.start_from_epoch + self.start
