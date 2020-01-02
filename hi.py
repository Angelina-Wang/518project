from custom_classes import *

client = HostClient('clienttt')
client.connectServer('10.0.0.3')
client.sendToServer('yello')


print("yo")
