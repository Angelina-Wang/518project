from custom_classes import *
import sys

client = AClient()
client.connectServer(sys.argv[1])
#client.restart(sys.argv[2])
client.startListener()
#msg1 = client.sendToServer('time')
#msg2 = client.sendToServer('hello')
#print(msg2)
