import socket
from handler import Handler
from utils import Message, Bytes
from linear_des import LinearDES


class Client():
  def __init__(self, host, port) -> None:
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.server_host = host
    self.server_port = port
    self.thread: Handler = None

    self.des = LinearDES('9182ye198ye289h12387e9')

  def stop(self):
    self.socket.shutdown(socket.SHUT_RDWR)

    if (self.thread):
      self.thread.stop()
      self.thread.join()

  def connect(self) -> bool:
    try:
      self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      try:
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
      except AttributeError:
        pass

      self.socket.connect((self.server_host, self.server_port))

      reply = Bytes.to_str(self.socket.recv(4096))
      sender = Message.get_sender(reply)

      if (sender == 'server'):
        content = Message.get_content(reply)

        print(content, '', end='')
        name = input()

        self.socket.sendall(Bytes.from_str(Message.create(name, name)))

        self.thread = Handler(self.socket, name, self.des)
        self.thread.start()

        return True

      else:
        return False

    except Exception:
      return False

  def send(self, message) -> None:
    message = self.des.encrypt(message)
    self.socket.send(Bytes.from_str(message))
