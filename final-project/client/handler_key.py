import threading
import socket
from typing import Dict, List, Set
from utils import Bytes, Request
from linear_des import LinearDES
from rsa import RSA, RSAClient
from copy import deepcopy


class HandlerKey(threading.Thread):
  def __init__(self, server_key_socket, name, client_des, client_key, client_keys, auth_key) -> None:
    threading.Thread.__init__(self)

    self.is_runnning = True
    self.server_key_socket: socket.socket = server_key_socket

    self.client_id: str = name
    self.client_des: LinearDES = client_des

    self.client_key: RSA = client_key
    self.auth_key: str = auth_key

    self.client_keys: Dict[str, RSAClient]  = client_keys 

  def stop(self) -> None:
    self.is_runnning = False
    self.server_key_socket.close()

  @staticmethod
  def update_keys(server_key_socket: socket.socket, client_id, client_keys, auth_key):
    for id in client_keys:
      if id != client_id and not client_keys[id]:
        request = Request.create_get(client_id, id)
        server_key_socket.sendall(Bytes.from_str(request))

        response = Bytes.to_str(server_key_socket.recv(4096))
        
        exp, mod = RSA.split_exp_mod_public(RSA.from_str(auth_key))
        response = RSA.decrypt_from(response, exp, mod)

        key = Request.validate_from_get(response, request)

        if (key):
          client_keys[id] = RSAClient(key)

  def check_clients(self):
    HandlerKey.update_keys(self.server_key_socket, self.client_id, self.client_keys, self.auth_key)

  def run(self) -> None:
    while self.is_runnning:
      try:
        self.check_clients()

      except Exception:
        pass
