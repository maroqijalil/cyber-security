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


p = 17055899557196527525682810191339089909014331959812898993437334555169285087976951946809555356817674844913188193949144165887100694620944167618997411049745043243260854998720061941490491091205087788373487296637817044103762239946752241631032791287021875863785226376406279424552454153388492970310795447866569138481
q = 171994050316145327367864378293770397343246561147593187377005295591120640129800725892235968688434055779668692095961697434700708550594137135605048681344218643671046905252163983827396726536078773766353616572531688390937410451433665914394068509329532352022301339189851111636176939179510955519440490431177444857017
rsa = RSA(p, q)
message = 'aasd38423h9nrh92038nry9834hn0rn89'

# Encrypting and decrypting
encrypted = rsa.encrypt(message) #Server uses private key to encrypt and decrypt messages
decrypted = rsa.decrypt(encrypted) #Clients use public key to encrypt and decrypt messages

print(message)
print(encrypted)
print(decrypted)

encrypted = rsa.sign(message) #Server uses private key to encrypt and decrypt messages
decrypted = rsa.verify(encrypted) #Clients use public key to encrypt and decrypt messages

print(message)
print(encrypted)
print(decrypted)
print(len('jalil,asd'.split(',')))

dict = {
    'jalil': None
}

print(dict)
print(dict['jalil'])