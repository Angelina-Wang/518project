from custom_classes import *
import sys

client = AClient()
client.connectServer(sys.argv[1])
msg = client.sendToServer(sys.argv[2])
print(msg)
client.close()
