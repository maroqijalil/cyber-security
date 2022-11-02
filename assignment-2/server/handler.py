import threading
import socket
from typing import List


class Handler(threading.Thread):
  def __init__(self, client_socket, target_sockets) -> None:
    threading.Thread.__init__(self)

    self.client_socket = client_socket
    self.target_sockets: List[socket.socket] = target_sockets
  
  def update_target_sockets(self, target_sockets) -> None:
    self.target_sockets = target_sockets

  def run(self) -> None:
    while True:
      request = self.client_socket.recv(4096)

      if request:
        response = f'Accepted {self.client_socket.getpeername()}'
        request = request.decode("utf-8")

        print(self.client_socket.getpeername(), end=": ")
        print(request)

        response = response.encode("utf-8")
        for target in self.target_sockets:
          target.sendall(response)

      else:
        self.client_socket.close()
        break
