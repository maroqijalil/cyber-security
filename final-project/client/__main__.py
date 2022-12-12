import argparse
import sys
from client import Client
import os
import tkinter as tk


parser = argparse.ArgumentParser(
    description='Connect TCPClient on defined host and port')
parser.add_argument(
    '--host', help='specify the host that will be connected to', type=str, default='localhost')
parser.add_argument(
    '--port', help='specify the port which is used', type=int, default=5000)
parser.add_argument(
    '--keyhost', help='specify the host key that will be connected to', type=str, default='localhost')
parser.add_argument(
    '--keyport', help='specify the port key which is used', type=int, default=6000)

args = parser.parse_args()

client = Client(args.host, args.port, args.keyhost, args.keyport)

try:
  if sys.platform == "win32":
    os.system('cls')
  else:
    os.system('clear')

  if client.connect():
    client.start()

    while True:
      client.send()
  
  else:
    client.stop()
    print('failed to connect')

except KeyboardInterrupt:
  client.stop()
  print()

  sys.exit(0)

except SystemExit:
  client.stop()
  print()

  sys.exit(0)
