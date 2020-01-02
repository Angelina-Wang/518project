import time
from scapy.sendrecv import sniff
import socket
from scapy.all import *

s = socket.socket()
port = 12345
#s.connect(('127.0.0.1', port))
s.connect(('10.0.0.3', port))
s.send("yes I am")
print(s.recv(1024))
s.close()

start = time.time()

def reset():
    start = time.time()

def get_time():
    t = time.time() - start
    return t

def call_func(pkt):
    print("hereeeee")
    print(pkt)
    print("------")
    #if IP in pkt and hasattr(pkt[IP], 'msg'):
    #    msg = pkt[IP].msg
    #    src = pkt[IP].src
    #    
    #    pkt = IP(dst=src) / TCP()
    #    pkt[IP].msg = get_time()
    #    
    #    send(pkt)

#sniff(prn=call_func, store=0)
