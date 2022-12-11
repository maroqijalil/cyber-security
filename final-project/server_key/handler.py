import threading
from typing import List, Dict, Tuple
from utils import Message, Bytes, Request
from rsa import RSA
import socket


class Handler(threading.Thread):
  def __init__(self, client_socket, client_keys, server_rsa, session_key) -> None:
    threading.Thread.__init__(self)

    self.client_socket: socket.socket = client_socket
    self.client_keys: Dict[str, str] = client_keys

    self.client_id = ''
    self.client_key = ''

    self.server_rsa: RSA = server_rsa
    self.session_key: str = session_key

  def stop(self) -> None:
    self.client_socket.close()

    for key in self.client_keys.keys():
      if key == self.client_id:
        del self.client_keys[key]

  def run(self) -> None:
    while True:
      message = self.client_socket.recv(4096)

      if message:
        message = Bytes.to_str(message)
        request = message.split(' ')
        response = ''

        if (request[0] == 'set'):
          self.client_id, self.client_key = Request.parse_set(request[1])
          self.client_keys[self.client_id] = self.client_key

          response = self.server_rsa.get_public_key()

          client_public_key: Tuple[int, int] = RSA.from_str(self.client_key)
          exp, mod = RSA.split_exp_mod_public(client_public_key)

          response = f'{response};{RSA.encrypt_from(self.session_key, exp, mod)}'

        elif (request[0] == 'get'):
          sender, target, _ = Request.parse_get(request[1])

          if (sender == self.client_id):
            response = Request.generate_from_get(self.client_keys.get(target), request[1])

        if (response):
          self.client_socket.sendall(Bytes.from_str(response))

      else:
        self.stop()
        break
