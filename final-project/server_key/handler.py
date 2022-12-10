import threading
from typing import List, Dict
from utils import Message, Bytes, Request


class Handler(threading.Thread):
  def __init__(self, client_socket, client_keys, auth_key) -> None:
    threading.Thread.__init__(self)

    self.client_socket = client_socket
    self.client_keys: Dict[str, str] = client_keys

    self.client_id = ''
    self.client_key = ''

    self.auth_key = auth_key

  def stop(self) -> None:
    self.client_socket.close()

    for key in self.client_keys.keys():
      if key == self.client_id:
        del self.client_keys[key]

  def send_message(self, message: str):
    print(self.client_id, Message.get_content(message))

    for target in self.client_keys:
      target.sendall(Bytes.from_str(message))

  def run(self) -> None:
    while True:
      message = self.client_socket.recv(4096)

      if message:
        message = Bytes.to_str(message)
        request = message.split(' ')
        reply = ''

        if (request[0] == 'set'):
          self.client_id, self.client_key = Request.parse_set(request[1])
          reply = self.auth_key

        elif (request[0] == 'get'):
          sender, target, _ = Request.parse_get(request[1])
          
          if (sender == self.client_id):
            reply = Request.generate_from_get(self.client_keys.get(target), request[1])
        
        if (reply):
          self.client_socket.sendall(reply)

      else:
        self.stop()
        break
