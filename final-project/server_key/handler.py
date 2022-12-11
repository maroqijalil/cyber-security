import threading
from typing import Dict, Tuple
from utils import Bytes, Request
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

    if self.client_id in self.client_keys:
      del self.client_keys[self.client_id]

  def run(self) -> None:
    while True:
      message = Bytes.to_str(self.client_socket.recv(4096))
      print(message)

      if message:
        request = message.split(' ')
        response = ''

        if (request[0] == 'set'):
          request = (' ').join(request[1:])

          self.client_id, self.client_key = Request.parse_set(request)
          self.client_keys[self.client_id] = self.client_key

          response = self.server_rsa.get_public_key()

          client_public_key: Tuple[int, int] = RSA.from_str(self.client_key)
          exp, mod = RSA.split_exp_mod_public(client_public_key)

          response = f'{response};{RSA.encrypt_from(self.session_key, exp, mod)}'

        elif (request[0] == 'get'):
          request = (' ').join(request[1:])
          sender, target, _ = Request.parse_get(request)

          if (sender == self.client_id):
            response = Request.generate_from_get(self.client_keys.get(target), request)
            response = self.server_rsa.sign(response)

        if (response):
          self.client_socket.sendall(Bytes.from_str(response))

      else:
        self.stop()
        break
