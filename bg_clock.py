import time
from scapy.sendrecv import sniff

start = time.time()

def reset():
    start = time.time()

def get_time():
    t = time.time() - start
    return t

def call_func(pkt):
    if hasattr(pkt[IP], 'msg'):
        msg = pkt[IP].msg
        src = pkt[IP].src
        
        pkt = IP(dst=src) / TCP()
        pkt[IP].msg = get_time()
        
        send(pkt)

sniff(prn=call_func, store=0)
