import threading
import socket
from typing import Dict, List, Set
from utils import Bytes, Request
from linear_des import LinearDES
from rsa import RSA


class HandlerKey(threading.Thread):
  def __init__(self, server_key_socket, name, client_des, client_key, client_keys, is_initator) -> None:
    threading.Thread.__init__(self)

    self.is_initator: bool = is_initator
    self.is_runnning = True
    self.server_key_socket: socket.socket = server_key_socket

    self.client_id: str = name
    self.client_des: LinearDES = client_des

    self.client_key: RSA = client_key

    self.client_keys: Dict[str, str]  = client_keys 

  def stop(self) -> None:
    self.is_runnning = False
    self.server_key_socket.close()

  def check_clients(self):
    for id in self.client_keys:
      if (id != self.client_id):
        request = Request.create_get(self.client_id, id)
        self.server_key_socket.sendall(Bytes.from_str(request))

        response = Bytes.to_str(self.server_key_socket.recv(4096))
        key = Request.validate_from_get(response, request)

        if (key):
          self.client_keys[id] = key

  def run(self) -> None:
    while self.is_runnning:
      self.check_clients()
