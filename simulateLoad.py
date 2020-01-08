from multiprocessing import Pool, cpu_count

def dummy(x):
    while True:
        x*x

processes = cpu_count()
pool = Pool(processes)
pool.map(dummy, range(processes))
