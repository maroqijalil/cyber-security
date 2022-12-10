import threading
import socket
from typing import List
from utils import Message, Bytes


class Handler(threading.Thread):
  def __init__(self, client_socket, target_sockets) -> None:
    threading.Thread.__init__(self)

    self.client_socket: socket.socket = client_socket
    self.target_sockets: List[socket.socket] = target_sockets

    self.client_name = ''
    self.greeting = False

  def stop(self) -> None:
    self.client_socket.close()

    for index, target in enumerate(self.target_sockets):
      if target == self.client_socket:
        del self.target_sockets[index]

  def send_message(self, message: str):
    print(self.client_name, Message.get_content(message))

    for target in self.target_sockets:
      target.sendall(Bytes.from_str(message))

  def run(self) -> None:
    while True:
      if (self.client_name):
        message = ''

        if (not self.greeting):
          self.greeting = True

          message = Message.create_greeting(self.client_name)

        else:
          reply = self.client_socket.recv(4096)

          if reply:
            reply = Bytes.to_str(reply)
            message = Message.create(self.client_name, reply)

          else:
            self.stop()
            break

        if (message):
          self.send_message(message)

      else:
        message = Message.create('server', 'Whats your name?')
        self.client_socket.sendall(Bytes.from_str(message))

        reply = Bytes.to_str(self.client_socket.recv(4096))
        self.client_name = Message.get_content(reply)
