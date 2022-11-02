import sys
import argparse
from server import Server
import os


parser = argparse.ArgumentParser(description='Run TCPServer on defined host and port')
parser.add_argument('--host', help='specify the host that will be used', type=str, default='localhost')
parser.add_argument('--port', help='specify the port which is used', type=int, default=5000)

args = parser.parse_args()

server = Server(args.host, args.port)

try:
  if server.connect():
    os.system('clear')

    while True:
      server.run()

except KeyboardInterrupt:
  print()
  
  sys.exit(0)
