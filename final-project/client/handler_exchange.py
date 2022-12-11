import threading
import socket
import os
import sys
from typing import Dict, List
from utils import Bytes, Message
from linear_des import LinearDES
from rsa import RSAClient


class HandlerExchange(threading.Thread):
  def __init__(self, server_socket, id, client_des, client_keys, target_id, is_initator) -> None:
    threading.Thread.__init__(self)

    self.server_socket: socket.socket = server_socket

    self.messages: List[Dict[str, str]] = []
    self.client_id: str = id

    self.client_des: LinearDES = client_des

    self.client_keys: Dict[str, RSAClient] = client_keys
    self.target_id = target_id

    self.is_initator = is_initator

  def run(self) -> None:
    if sys.platform == "win32":
      os.system('cls')
    else:
      os.system('clear')

    reply = Bytes.to_str(self.server_socket.recv(4096))

    if reply:
      sender = Message.get_sender(reply)
      content = Message.get_content(reply)

      self.messages.append({sender: content})

    else:
      self.server_socket.close()
