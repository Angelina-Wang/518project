from mininet.node import Host
import time

class HostWithTime(Host):
	def __init__(self, name, inNamespace=True, **params):
		super(HostWithTime, self).__init__(name, inNamespace, **params)
		self.start = 0
		self.start_from_epoch = time.time()

	def restart(self, start):
		self.start = start
		self.start_from_epoch = time.time()

	def getTime(self):
		return time.time() - self.start_from_epoch + self.start
