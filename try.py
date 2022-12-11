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

    self.max_msg = 0

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
    self.max_msg = len(str(self.n))
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
  def __init__(self, public_key: str) -> None:
    self.is_paired = False
    self.public_key = public_key
    self.n, self.e = RSA.from_str(public_key)

    self.n_verification = random.randint(0, self.n)

  def get_pair_request():
    pass


# 400 digits
p = 1357911131517193133353739515355575971737577799193959799111113115117119131133135137139151153155157159171173175177179191193195197199311313315317319331333335337339351353355357359371373375377379391393395397399511513515517519531533535537539551553555557559571573575577579591593595597599711713715717719731733735737739751753755757759771
q = 199999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
rsa = RSA(p, q)

message = 879823794827398239847777777777777777777777777777777777777777777777777777777

encrypted = rsa.encrypt(message)
decrypted = rsa.decrypt(encrypted)

print(message)
print(encrypted)
print('decrypted', decrypted)


# import secrets

# message = secrets.token_hex(64)

# # message = '171994050316145327367864378293770397343246561147593187377005295591120640129800725892235968688434055779668692095961697434700708550594137135605048681344218643671046905252163983827396726536078773766353616572531688390937410451433665914394068509329532352022301339189851111636176939179510955519440490431177444857017alajshdkahfkhfkwbefsjkAfbhksjNFAKfbfsJBefkukwehfwjjakjqq231t3637589859'
# message = '(2933513246627580364141974824910272334944648573837141561255927138093643428389882442532446759321663580026646253077539733478646046838901209715307512740250307916924674115916046854359376264328491788268404554366593628833650344268448520682993862241435054440816010317783165801561057550380452945181206714627220741848482621747665654478085244249912121627789573223463987569166004326122297788297874357032506957023557064148741513238491976898626467312319402714944362795834726817679223085655608261564486969006826933694646990281711696072037411032697341174880051797006066311547679943648623234590207135954434021238012213783105917571177, 2154189025879244979622258397587670225742529464515800212061812419097417141336825768694523052275976013182005839418362653457625192949625732998434918295288841781730857589778592991497198811424930811928390076539418490734511005765454041439806618106123019301869367522485839250307671656911170174146753357853245297421575076898970433509267696050851109925399564450081188086769585371438272574977989287852908044241010218449000456806688201940301964878339504375064576199174734823261120937594051098852563634104592302467829972909265086750421879380986618725956159127793871562137735770213394764882345194742686614751342048772712006874551);k;j;Sun Dec 11 16:30:31 2022'
# print('hai',(rsa.max_msg - 1)/3)
# print(len(message))

# msg = message
# res_encrypted = ''
# res_decrypted = ''
# max_iter = (rsa.max_msg - 1)//3
# while max_iter % 3 != 0:
#     max_iter -= 1

# print(max_iter)

# while msg != '':
#   now = msg[:max_iter]
#   # Encrypting and decrypting
#   encrypted = rsa.encrypt(now) #Server uses private key to encrypt and decrypt messages
#   res_encrypted += encrypted

#   msg = msg[max_iter:]

# msg = str(res_encrypted)
# while msg != '':
#   now = msg[:max_iter]
#   decrypted = rsa.decrypt(int(now)) #Clients use public key to encrypt and decrypt messages
#   res_decrypted += str(decrypted)

#   msg = msg[max_iter:]
# # print(message)
# # print(res_encrypted)
# print()
# print(res_decrypted)

# encrypted = rsa.sign(message) #Server uses private key to encrypt and decrypt messages
# decrypted = rsa.verify(encrypted) #Clients use public key to encrypt and decrypt messages

# print(message)
# print(encrypted)
# print(decrypted)
