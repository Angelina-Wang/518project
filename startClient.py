from custom_classes import *

client = AClient()
client.connectServer('10.0.0.3')
msg1 = client.sendToServer('time')
msg2 = client.sendToServer('hello')
print(msg2)

