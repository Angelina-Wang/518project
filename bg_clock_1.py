import time
from scapy.sendrecv import sniff
import socket
from scapy.all import *

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345
#sock1.bind(('', port))
sock1.bind(('0.0.0.0', port))
sock1.listen(1)
print 'socket is listening'

c, addr = sock1.accept()
print 'got connection from', addr
c.send("Hello are you there")
response = c.recv(4096)
print(response)
c.close()

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
