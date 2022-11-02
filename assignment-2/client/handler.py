import threading
import socket
import os
from typing import Dict, List


class Handler(threading.Thread):
  def __init__(self, server_socket, name) -> None:
    threading.Thread.__init__(self)

    self.server_socket: socket.socket = server_socket
    self.is_runnning = True

    self.messages: List[Dict[str, str]] = []
    self.name = name

  def stop(self) -> None:
    self.is_runnning = False
    self.server_socket.close()
  
  def run(self) -> None:
    while self.is_runnning:
      reply = self.server_socket.recv(4096)

      if reply:
        os.system('clear')
        print(reply.decode("utf-8"))

      else:
        self.server_socket.close()
        break
