import numpy as np

def getTimesMultiple(command, server, clientList):
    diffs = []
    for client in clientList:
        a = time.time()
        serverTime = float(command.cmd('python startCommander.py {0} {1}'.format(server.IP(), 'getTime')))
        b = time.time()
        clientTime = float(command.cmd('python startCommander.py {0} {1}'.format(client.IP(), 'getTime')))
        c = time.time()

        serverAdjust = serverTime + (b-a)/2.
        clientAdjust = clientTime - (c-b)/2.
        
        diffs.append(np.abs(serverAdjust-clientAdjust))

    return diffs