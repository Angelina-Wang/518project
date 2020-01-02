from custom_classes import *

client = AClient()
client.connectServer('10.0.0.3')
print(client.sendToServer('time'))

