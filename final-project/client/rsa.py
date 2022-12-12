import random
import math
import ast
from typing import Tuple


class RSA:
  @staticmethod
  def to_str(key):
    return str(key)

  @staticmethod
  def from_str(key):
    return ast.literal_eval(key)

  @staticmethod
  def split_exp_mod_public(key: Tuple[int, int]):
    return key[1], key[0]

  @staticmethod
  def split_exp_mod_private(key: Tuple[int, int, int]):
    return key[2], key[0] * key[1]
  
  @staticmethod
  def encrypt_from(m, exp, mod):
    is_str = False

    if isinstance(m, str):
      is_str = True

      plain = [str(ord(l)).ljust(3, '0') for l in m]
      m = int(''.join(plain))

    encrypted = pow(m, exp, mod)

    if is_str:
      encrypted = str(encrypted)

    return encrypted

  @staticmethod
  def decrypt_from(c, exp, mod):
    is_str = False

    if isinstance(c, str):
      is_str = True
      c = int(c)

    decrypted = pow(c, exp, mod)

    if is_str:
      dc_raw = str(decrypted)
      dc_str = ''

      while dc_raw != '':
        p = dc_raw[:3]
      
        if (int(p) > 128):
          dc_str += chr(int(p)//10)
      
        else: 
          dc_str += chr(int(p))
        dc_raw = dc_raw[3:]

      decrypted = dc_str

    return decrypted

  def __init__(self, p, q):
    self.p = p
    self.q = q

    self.e = self.d = self.n = 0
    self.is_msg_str = False

    self.__generate_keys()

  def __modular_inverse(self, A, M):
    m0 = M
    y = 0
    x = 1

    if (M == 1):
      raise Exception('modular inverse does not exist')
    
    while (A > 1):
      q = A // M
      
      temp = M 
      M = A % M
      A = temp
      
      temp = y
      y = x - q * y
      x = temp
    
    if (x < 0):
      x = x + m0
    
    return x
  
  def __generate_keys(self):
    self.n = self.p * self.q
    self.phi_n = (self.p - 1) * (self.q - 1)

    self.e = random.randint(2, self.phi_n - 1)
    while math.gcd(self.e, self.phi_n) != 1:
      self.e = random.randint(2, self.phi_n - 1)

    self.d = self.__modular_inverse(self.e, self.phi_n)

  def encrypt(self, m, sign = False):
    exp, mod = RSA.split_exp_mod_public(self.get_public_key())

    if sign:
      exp, mod = RSA.split_exp_mod_private(self.get_private_key())

    return RSA.encrypt_from(m, exp, mod)

  def decrypt(self, c, sign = False):
    exp, mod = RSA.split_exp_mod_private(self.get_private_key())

    if sign:
      exp, mod = RSA.split_exp_mod_public(self.get_public_key())

    return RSA.decrypt_from(c, exp, mod)

  def sign(self, m):
    return self.encrypt(m, True)

  def verify(self, c):
    return self.decrypt(c, True)

  def get_public_key(self):
    return self.n, self.e

  def get_private_key(self):
    return self.p, self.q, self.d
  
  def maximum_bits(self):
    return self.n.bit_length()


class RSAClient:
  def __init__(self, id, target_id, target_public_key: str) -> None:
    self.is_paired = False
    self.is_initator = False
    self.id = id

    self.target_id = target_id
    self.target_public_key = target_public_key
    self.n, self.e = RSA.from_str(target_public_key)

    self.n_verification = random.randint(0, 1000)

  def create_request(self, message: str):
    exp, mod = RSA.split_exp_mod_public(RSA.from_str(self.target_public_key))
    return RSA.encrypt_from(message, exp, mod)

  def create_key_response(self, message: str, key):
    messages = message.split(';')
    return self.create_request(f'{messages[1]};{key}')

  def get_pair_request(self, message: str = ''):
    if self.is_initator:
      message = f'{self.id};{self.n_verification}'

    else:
      messages = message.split(';')
      message = f'{messages[1]};{self.n_verification}'

    return self.create_request(message)
  
  def verify_pair_request(self, message: str):
    messages = message.split(';')

    if self.is_initator:
      message = messages[0]
      return message == f'{self.n_verification}'
    
    else:
      message = messages[0]
      return message == self.target_id
  
  def verify_key_response(self, message: str):
    messages = message.split(';')

    if len(messages) == 2:
      message = messages[0]
      return message == f'{self.n_verification}'

    return False

  @staticmethod
  def get_session_key(message: str):
    return message.split(';')[1]
