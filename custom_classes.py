from mininet.node import Host
import time

class HostWithTime(Host):
	def __init__(self, start):
		super().__init__()
		self.start = start
		self.start_from_epoch = time.time()

	def restart(self, start):
		self.start = start
		self.start_from_epoch = time.time()

	def get_time(self):
		return time.time() - self.start_from_epoch + self.start