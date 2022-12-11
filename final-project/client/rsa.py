import random
import math
import ast


class RSA:
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
    is_str = False

    if isinstance(m, str):
      is_str = True

      plain = [str(ord(l)).ljust(3, '0') for l in m]
      m = int(''.join(plain))
  
    exp = self.e
    mod = self.n

    if sign:
      exp = self.d
      mod = self.p * self.q

    encrypted = pow(m, exp, mod)

    if is_str:
      encrypted = str(encrypted)

    return encrypted

  def decrypt(self, c, sign = False):
    is_str = False

    if isinstance(c, str):
      is_str = True
      c = int(c)

    exp = self.d
    mod = self.p * self.q

    if sign:
      exp = self.e
      mod = self.n

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

  @staticmethod
  def to_str(key):
    return str(key)

  @staticmethod
  def from_str(key):
    return ast.literal_eval(key)


class RSAClient:
  def __init__(self, public_key: str) -> None:
    self.is_paired = False
    self.public_key = public_key
    self.n, self.e = RSA.from_str(public_key)

    self.n_verification = random.randint(0, self.n)

  def get_pair_request():
    pass
