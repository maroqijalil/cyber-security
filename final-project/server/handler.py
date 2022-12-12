import threading
import socket
from typing import List, Dict
from utils import Message, Bytes


class Handler(threading.Thread):
  def __init__(self, client_socket, target_sockets, client_names) -> None:
    threading.Thread.__init__(self)

    self.client_socket: socket.socket = client_socket

    self.target_sockets: Dict[str, socket.socket] = target_sockets
    self.client_names: List[str] = client_names

    self.client_name = ''

  def stop(self) -> None:
    self.client_socket.close()

    del self.target_sockets[self.client_name]

    message = Message.create_farewell(self.client_name)
    self.send_message(message)

  def send_message(self, message: str):
    print(self.client_name, Message.get_content(message))

    for target in self.target_sockets:
      self.target_sockets[target].sendall(Bytes.from_str(message))

  def run(self) -> None:
    message = Message.create('server', 'Whats your name?')
    self.client_socket.sendall(Bytes.from_str(message))

    reply = Bytes.to_str(self.client_socket.recv(4096))
    self.client_name = Message.get_content(reply)

    self.target_sockets[self.client_name] = self.client_socket

    self.client_names.append(self.client_name)

    content = ''
    if len(self.client_names) > 1:
      content = self.client_names[0]

    message = Message.create('server', content)
    self.client_socket.sendall(Bytes.from_str(message))

    message = Message.create_greeting(self.client_name)
    self.send_message(message)

    while True:
      reply = Bytes.to_str(self.client_socket.recv(4096))

      if Message.is_exchange(reply):
        content = Message.get_content(reply)
        contents = content.split(';')

        if len(contents) == 2:
          reply = Message.create_exchange(self.client_name, contents[1])
          self.target_sockets[contents[0]].sendall(Bytes.from_str(reply))

      else:
        message = ''

        if reply:
          message = Message.create(self.client_name, reply)

        else:
          self.stop()
          break

        if (message):
          self.send_message(message)
