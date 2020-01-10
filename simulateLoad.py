"""

from multiprocessing import Pool, cpu_count
import sys

def dummy(x):
    while True:
        x*x

print(cpu_count())
processes = int(cpu_count() * float(sys.argv[1]))
pool = Pool(processes)
pool.map(dummy, range(processes))
"""

from threading import Thread
import sys

def dummy():
    x = 1.000000001
    while True:
        x*=x

for i in range(sys.argv[1]):
    t1 = Thread(target=dummy)
    t1.setDaemon(True)
