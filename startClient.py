from custom_classes import *
import sys

client = AClient()
client.connectServer(sys.argv[1])
client.restart(float(sys.argv[2]))
client.startListener()
