import time
import socket
import asyncore
import logging
import threading
import pdb
from handler import EchoHandler
import sys

class EchoClient(asyncore.dispatcher):
    """Sends messages to the server and receives responses.
    """
    
    def __init__(self, start_time, host, port):
        self.start_offset = start_time
        self.to_send = None

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.chunk_size = 256
        
        return

    def run_ntp(self):
        self.to_send = 'sntp'

    def get_time(self):
        return self.start_offset + time.time()
    
    def handle_connect(self):
        self.run_ntp()
        return
    
    def handle_close(self):
        self.close()
        return

    def writable(self):
        # called by the handler to see if there is data that the client wants
        # to write
        return self.to_send is not None

    def handle_write(self):
        self.start_ntp = self.get_time()
        sent = self.send('sntp') # message to start ntp
        print('sending', sent)
        self.to_send = None # once ntp is started we have nothing left to write

    def handle_read(self):
        recv_ntp = self.recv(self.chunk_size)
        print('received', recv_ntp)
        sent_ntp = self.recv(self.chunk_size)
        print('received', sent_ntp)
        self.end_ntp = self.get_time()

        # perform ntp with the two timestamps the server gives
        two_delta = (self.end_ntp - self.start_ntp) - (sent_ntp - recv_ntp)
        self.start_offset = sent_ntp + 0.5*two_delta

        print(self.get_time())

loop_thread = threading.Thread(target=asyncore.loop)
loop_thread.start()

c = EchoClient(int(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3]))
