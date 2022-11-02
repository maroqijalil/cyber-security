import threading
import socket
from typing import List


class Handler(threading.Thread):
  def __init__(self, client_socket, target_sockets) -> None:
    threading.Thread.__init__(self)

    self.client_socket = client_socket
    self.target_sockets: List[socket.socket] = target_sockets

  def stop(self) -> None:
    self.client_socket.close()

    for index, target in enumerate(self.target_sockets):
      if target == self.client_socket:
        del self.target_sockets[index]

  def run(self) -> None:
    while True:
      request = self.client_socket.recv(4096)

      if request:
        response = f'Accepted {self.client_socket.getpeername()}'
        request = request.decode("utf-8")

        print(self.client_socket.getpeername(), end=": ")

        response = response.encode("utf-8")
        for target in self.target_sockets:
          if target != self.client_socket:
            target.sendall(response)

      else:
        self.stop()
        break
