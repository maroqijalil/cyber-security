import threading
import socket
import os
import sys
from typing import Dict, List
from utils import Bytes, Message
from linear_des import LinearDES
from rsa import RSAClient


class Handler(threading.Thread):
  def __init__(self, server_socket, name, client_des: LinearDES, client_keys) -> None:
    threading.Thread.__init__(self)

    self.server_socket: socket.socket = server_socket
    self.is_runnning = True

    self.messages: List[Dict[str, str]] = []
    self.client_name = name

    self.client_des = client_des
    self.client_keys: Dict[str, RSAClient] = client_keys

  def stop(self) -> None:
    self.is_runnning = False
    self.server_socket.close()

  def filter_sender(self, sender) -> str:
    if (sender == self.client_name):
      return 'You'

    else:
      return sender

  def print_messages(self):
    if sys.platform == "win32":
      os.system('cls')
    else:
      os.system('clear')

    for message in self.messages:
      for sender, content in message.items():
        if (Message.is_greeting(content)):
          print()
          print(f'\t{self.filter_sender(sender)}', content)
          print()

          self.client_keys[sender] = None

        else:
          print(f'{self.filter_sender(sender)}:', self.client_des.decrypt(content))

    print()
    print('>> ')

  def run(self) -> None:
    while self.is_runnning:
      reply = Bytes.to_str(self.server_socket.recv(4096))

      if reply:
        sender = Message.get_sender(reply)
        content = Message.get_content(reply)

        self.messages.append({sender: content})

        self.print_messages()

      else:
        self.server_socket.close()
        break
