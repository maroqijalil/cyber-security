import socket
from handler import Handler
from handler_key import HandlerKey
from utils import Message, Bytes, Request
from linear_des import LinearDES
from typing import List, Dict
from rsa import RSA, RSAClient


class Client():
  def __init__(self, host, port, key_host, key_port) -> None:
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.name = ''

    self.server_host = host
    self.server_port = port
    self.thread: Handler = None

    self.socket_key = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.server_key_host = key_host
    self.server_key_port = key_port
    self.thread_key: HandlerKey = None

    # 48 digits
    p = 786287537753406666185810464356342863432256602639
    q = 585724299028731854439673592969136581559573957839
    self.client_rsa = RSA(p, q)

    self.auth_key = ''
    self.client_keys: Dict[str, RSAClient] = {}
    self.is_initator: bool = False

    self.client_des: LinearDES = None

  def stop(self):
    self.socket.shutdown(socket.SHUT_RDWR)

    if (self.thread):
      self.thread.stop()
      self.thread.join()

    self.socket_key.shutdown(socket.SHUT_RDWR)

    if (self.thread_key):
      self.thread_key.stop()
      self.thread_key.join()

  def connect(self) -> bool:
    try:
      self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.socket_key.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      
      try:
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.socket_key.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
      
      except AttributeError:
        pass

      self.socket.connect((self.server_host, self.server_port))
      self.socket_key.connect((self.server_key_host, self.server_key_port))

      reply = Bytes.to_str(self.socket.recv(4096))
      sender = Message.get_sender(reply)

      if (sender == 'server'):
        content = Message.get_content(reply)

        print(content, '', end='')
        self.name = input()

        self.socket.sendall(Bytes.from_str(Message.create(self.name, self.name)))
        reply = Bytes.to_str(self.socket.recv(4096))
        sender = Message.get_sender(reply)

        if (sender == 'server'):
          content = Message.get_content(reply)
          self.is_initator = not bool(content)

          if content:
            self.client_keys[content] = None

        self.socket_key.sendall(Bytes.from_str(Request.create_set(self.name, str(self.client_rsa.get_public_key()))))
        responses = Bytes.to_str(self.socket_key.recv(4096)).split(';')

        self.auth_key = responses[0]
        if len(responses) > 1 and self.is_initator:
          self.client_des = LinearDES(self.client_rsa.decrypt(responses[1]))

        if self.client_des:
          self.thread = Handler(self.socket, self.name, self.client_des, self.client_keys)
          self.thread.start()

        if self.is_initator:
          self.thread_key = HandlerKey(self.socket_key, self.name, self.client_des, self.client_rsa, self.client_keys, self.auth_key)
          self.thread_key.start()

        return True

      else:
        return False

    except Exception:
      return False

  def handle_exchange(self):
    for id in self.client_keys:
      if id != self.name and self.client_keys[id] and not self.client_keys[id].is_paired:
        pass

  def send(self) -> None:
    if self.client_des:
      print('>> ', end='')
      message = self.client_des.encrypt(input())
      self.socket.send(Bytes.from_str(message))
    
    else:
      HandlerKey.update_keys(self.socket_key, self.name, self.client_keys, self.auth_key)
      self.handle_exchange()
    
    if self.is_initator:
      try:
        self.handle_exchange()

      except Exception:
        pass
