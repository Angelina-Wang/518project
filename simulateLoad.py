from threading import Thread
import sys

def dummy():
    x = 1.000000001
    while True:
        x*=x

for i in range(sys.argv[1]):
    t1 = Thread(target=dummy)
    t1.setDaemon(True)
