from custom_classes import *

client = AClient()
client.connectServer('10.0.0.4')
client.startListener()
#msg1 = client.sendToServer('time')
#msg2 = client.sendToServer('hello')
#print(msg2)
