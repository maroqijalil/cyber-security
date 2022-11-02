import threading


class Handler(threading.Thread):
  def __init__(self, server_socket) -> None:
    threading.Thread.__init__(self)

    self.server_socket = server_socket
    self.is_runnning = True

  def stop(self) -> None:
    self.is_runnning = False
    self.server_socket.close()
  
  def run(self) -> None:
    while self.is_runnning:
      response = self.server_socket.recv(4096)

      if response:
        print(response.decode("utf-8"))

      else:
        self.server_socket.close()
        break
