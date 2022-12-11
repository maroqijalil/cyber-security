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

    self.server_host = host
    self.server_port = port
    self.thread: Handler = None

    self.socket_key = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.server_key_host = key_host
    self.server_key_port = key_port
    self.thread_key: HandlerKey = None

    p = 17055899557196527525682810191339089909014331959812898993437334555169285087976951946809555356817674844913188193949144165887100694620944167618997411049745043243260854998720061941490491091205087788373487296637817044103762239946752241631032791287021875863785226376406279424552454153388492970310795447866569138481
    q = 171994050316145327367864378293770397343246561147593187377005295591120640129800725892235968688434055779668692095961697434700708550594137135605048681344218643671046905252163983827396726536078773766353616572531688390937410451433665914394068509329532352022301339189851111636176939179510955519440490431177444857017
    self.client_rsa = RSA(p, q)
    self.auth_key = ''

    self.client_des: LinearDES = None

    self.client_keys: Dict[str, RSAClient] = {}

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
      self.socket_key.connect((self.server_host, self.server_port))

      reply = Bytes.to_str(self.socket.recv(4096))
      sender = Message.get_sender(reply)

      if (sender == 'server'):
        content = Message.get_content(reply)

        print(content, '', end='')
        name = input()

        self.socket.sendall(Bytes.from_str(Message.create(name, name)))
        reply = Bytes.to_str(self.socket.recv(4096))
        sender = Message.get_sender(reply)

        if (sender == 'server'):
          content = Message.get_content(reply)
          content = content.split(',')

          self.socket_key.sendall(Bytes.from_str(Request.create_set(name, str(self.client_rsa.get_public_key()))))
          responses = Bytes.to_str(self.socket_key.recv(4096)).split(';')

          self.auth_key = responses[0]
          if len(responses) > 1:
            self.client_des = LinearDES(self.client_rsa.decrypt(responses[1]))

          if self.client_des:
            self.thread_key = HandlerKey(self.socket_key, name, self.client_des, self.client_rsa, self.client_keys, len(content) == 1)
            self.thread_key.start()

            self.thread = Handler(self.socket, name, self.client_des, self.client_keys)
            self.thread.start()

            return True

      else:
        return False

    except Exception:
      return False

  def send(self, message) -> None:
    message = self.client_des.encrypt(message)
    self.socket.send(Bytes.from_str(message))
