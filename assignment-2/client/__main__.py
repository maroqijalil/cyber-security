import argparse
import sys
from client import Client


parser = argparse.ArgumentParser(description='Connect TCPClient on defined host and port')
parser.add_argument('--host', help='specify the host that will be connected to', type=str, default='localhost')
parser.add_argument('--port', help='specify the port which is used', type=int, default=5000)

args = parser.parse_args()

client = Client(args.host, args.port)

try:
  if client.connect():
    while True:
      print('>> ', end='')
      client.command(input())

except KeyboardInterrupt:
  client.stop()
  sys.exit(0)
