import socket
import select
from typing import List
from handler import Handler


class Server():
  def __init__(self, host, port) -> None:
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.host = host
    self.port = port

    self.target_sockets: List[socket.socket] = []
    self.client_threads: List[Handler] = []

  def __del__(self):
    self.server_socket.close()

  def connect(self) -> bool:
    try:
      self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      try:
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
      except AttributeError:
        pass

      self.server_socket.bind((self.host, self.port))
      self.server_socket.listen(100)

      return True

    except Exception:
      return False

  def run(self):
    is_running = True

    while is_running:
      try:
        read_ready_sockets, _, _ = select.select([self.server_socket], [], [])

        for ready_socket in read_ready_sockets:
          if ready_socket == self.server_socket:
            client_socket, _ = self.server_socket.accept()

            client = Handler(client_socket, self.target_sockets)
            client.start()
            self.client_threads.append(client)

            self.target_sockets.append(client_socket)

      except KeyboardInterrupt:
        is_running = False

    self.server_socket.close()
    for client in self.client_threads:
      client.join()
