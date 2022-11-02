import argparse
import sys
from client import Client
import os


parser = argparse.ArgumentParser(
    description='Connect TCPClient on defined host and port')
parser.add_argument(
    '--host', help='specify the host that will be connected to', type=str, default='localhost')
parser.add_argument(
    '--port', help='specify the port which is used', type=int, default=5000)

args = parser.parse_args()

client = Client(args.host, args.port)

try:
  os.system('clear')

  if client.connect():
    while True:
      print('>> ', end='')
      client.send(input('>> '))

except KeyboardInterrupt:
  client.stop()
  print()

  sys.exit(0)
