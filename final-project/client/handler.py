import threading
import socket
import os
import sys
from typing import Dict, List
from utils import Bytes, Message
from linear_des import LinearDES
from rsa import RSAClient


class Handler(threading.Thread):
  def __init__(self, server_socket, name, client_des: LinearDES, client_keys, message_exchanges) -> None:
    threading.Thread.__init__(self)

    self.server_socket: socket.socket = server_socket
    self.is_runnning = True

    self.messages: List[Dict[str, str]] = []
    self.client_name = name

    self.client_des = client_des
    self.client_keys: Dict[str, RSAClient] = client_keys

    self.message_exchanges: Dict[str, List[str]] = message_exchanges

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

          if sender not in self.client_keys:
            self.client_keys[sender] = None

        elif (Message.is_farewell(content)):
          print()
          print(f'\t{self.filter_sender(sender)}', content)
          print()

          if sender in self.client_keys:
            del self.client_keys[sender]

        elif self.client_des.key:
          print(f'{self.filter_sender(sender)}:', self.client_des.decrypt(content))

    print()
    print('>> ')

  def run(self) -> None:
    while self.is_runnning:
      reply = Bytes.to_str(self.server_socket.recv(4096))

      if reply:
        sender = Message.get_sender(reply)
        content = Message.get_content(reply)

        if Message.is_exchange(reply):
          contents = content.split(';')

          if len(contents) == 2:
            if contents[0] in self.message_exchanges:
              self.message_exchanges[contents[0]].append(contents[1])

            else:
              self.message_exchanges[contents[0]] = [contents[1]]

        else:
          self.messages.append({sender: content})
          self.print_messages()

      else:
        self.server_socket.close()
        break
