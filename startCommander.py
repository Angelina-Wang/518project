from custom_classes import *

client = AClient()
client.connectServer('10.0.0.1')
msg1 = client.sendToServer('time')
print(msg1)
#msg2 = client.sendToServer('hello')
#print(msg2)

