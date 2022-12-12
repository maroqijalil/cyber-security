import threading
import socket
import os
import sys
from typing import Dict, List
from utils import Bytes, Message
from linear_des import LinearDES
from rsa import RSAClient, RSA


class HandlerExchange(threading.Thread):
  def __init__(self, server_socket, id, client_rsa, client_des, client_keys, target_id, is_initator, message_exchanges) -> None:
    threading.Thread.__init__(self)

    self.server_socket: socket.socket = server_socket

    self.messages: List[Dict[str, str]] = []
    self.client_id: str = id
    self.client_rsa: RSA = client_rsa

    self.client_des: LinearDES = client_des

    self.client_keys: Dict[str, RSAClient] = client_keys
    self.target_id = target_id

    self.is_initator = is_initator

    self.message_exchanges: Dict[str, List[str]] = message_exchanges
    self.message_step = 0

    if self.target_id not in self.message_exchanges:
      self.message_exchanges[self.target_id] = []

  def stop(self):
    self.message_step = 4

  def get_response(self, index):
    reply = self.message_exchanges[self.target_id][index]
    return self.client_rsa.decrypt(reply)

  def send_request(self, request: str):
    message = Message.create_exchange(self.target_id, request)
    self.server_socket.sendall(Bytes.from_str(message))

  def run(self) -> None:
    try:
      target_client = self.client_keys[self.target_id]
      reply = ''

      while self.message_step < 4:
        if self.is_initator:
          if self.message_step == 0:
            request = target_client.get_pair_request()

            self.send_request(request)
            self.message_step += 1
          
          elif self.message_step == 1:
            if self.message_exchanges[self.target_id]:
              reply = self.get_response(0)

              if reply and target_client.verify_pair_request(reply):
                self.message_step += 1

          elif self.message_step == 2:
            request = target_client.create_key_response(reply, self.client_des.key)
            self.send_request(request)

            self.message_step += 1

          elif self.message_step == 3:
            if len(self.message_exchanges[self.target_id]) > 1:
              reply = self.get_response(1)

              if reply:
                self.client_keys[self.target_id].is_paired = reply == self.client_des.key
                self.message_step += 1

        else:
          if self.message_step == 0:
            if self.message_exchanges[self.target_id]:
              reply = self.get_response(0)
            
              if reply and target_client.verify_pair_request(reply):
                self.message_step += 1

          elif self.message_step == 1:
            request = target_client.get_pair_request(reply)

            self.send_request(request)
            self.message_step += 1

          elif self.message_step == 2:
            if len(self.message_exchanges[self.target_id]) > 1:
              reply = self.get_response(1)

              if (target_client.verify_key_response(reply)):
                self.message_step += 1

          elif self.message_step == 3:
            session_key = RSAClient.get_session_key(reply)
            self.client_des.key = session_key
            self.client_des.init()

            request = target_client.create_request(session_key)
            self.send_request(request)
            self.message_step += 1

    except Exception:
      pass
