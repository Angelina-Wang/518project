from custom_classes import *
import sys

client = AClient()
client.connectServer(sys.argv[1])
msg1 = client.sendToServer('startNTP')
print(msg1)
client.close()
#msg2 = client.sendToServer('hello')
#print(msg2)

