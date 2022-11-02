import socket
from handler import Handler


class Client():
  def __init__(self, host, port) -> None:
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.server_host = host
    self.server_port = port
    self.thread: Handler = None
  
  def stop(self):
    self.socket.shutdown(socket.SHUT_RDWR)

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
      
      self.thread = Handler(self.socket)
      self.thread.start()

      return True

    except Exception:
      return False
  
  def command(self, command) -> None:
    self.socket.send(command.encode('utf-8'))
