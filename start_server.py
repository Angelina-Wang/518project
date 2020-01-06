import time
import socket
import asyncore
import logging
import threading
import pdb
from handler import EchoHandler
import sys

class EchoServer(asyncore.dispatcher):
    """Receives connections and establishes handlers for each client.
    """
    
    def __init__(self, start_time):
        asyncore.dispatcher.__init__(self)
        
        self.ntp = False # are we running NTP right now
        self.recv_ntp = None
        self.send_ntp = None
        self.start_offset = start_time

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('0.0.0.0', 8080))
        self.address = self.socket.getsockname()
        self.listen(1)
        
        return

    def get_time(self):
        return self.start_offset + time.time()

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        EchoHandler(sock=client_info[0])
        return
    
    def handle_close(self):
        self.close()
        return

    def writable(self):
        return self.ntp

    def handle_write(self):
        assert self.recv_ntp is not None
        sent = self.send(self.recv_ntp)
        self.send_ntp = self.get_time()
        sent = self.send(self.send_ntp)
        self.ntp = False
        self.recv_ntp = None
        self.send_ntp = None

    def handle_read(self):
        msg = self.recv(4)
        if msg == 'sntp':
            self.recv_ntp = self.get_time()
            self.ntp = True

loop_thread = threading.Thread(target=asyncore.loop)
loop_thread.start()

server = EchoServer(int(sys.argv[1]))
