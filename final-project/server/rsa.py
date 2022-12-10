import random
import math

class RSA:
    def __init__(self):
        self.e = self.d = self.p = self.q = self.phi_n = 0
        self.is_msg_str = False
    
    def __mod_inv(self, A, M):
        # e, phi_n; d = 1 mod phi_n / e
        m0 = M
        y = 0
        x = 1

        if (M == 1):
          return 0
        
        while (A > 1):
          q = A // M
          t = M 

          M = A % M
          A = t
          t = y

          y = x - q * y
          x = t
        
        if (x < 0):
          x = x + m0
        
        return x
    
    def generate_keys(self, p, q):
        self.p = p
        self.q = q
        self.n = self.p * self.q

        self.phi_n = (self.p - 1) * (self.q - 1)

        # since e is chosen randomly, we repeat the random choice until e is (not share a factor) coprime to phi_n.
        self.e = random.randint(2, self.phi_n - 1)
        while math.gcd(self.e, self.phi_n) != 1:
            self.e = random.randint(2, self.phi_n - 1)

        self.d = self.__mod_inv(self.e, self.phi_n)
        print((self.e * self.d) % self.phi_n == 1)

    def encrypt(self, m, public_key=None):
        if (public_key == None):
            public_key[0] = self.n
            public_key[1] = self.e

        if isinstance(m, str):
          self.is_msg_str = True
          plain = [str(ord(l)).ljust(3, '0') for l in m]
          m = int(''.join(plain))
          print("m in num : ", m)
      
        encrypted = pow(m, public_key[1], public_key[0])

        return encrypted  # encrypted

    def decrypt(self, c, private_key=None):
        if (private_key == None):
            private_key[0] = self.p
            private_key[1] = self.q
            private_key[2] = self.d

        decrypted = pow(c, private_key[2], private_key[0] * private_key[1])
        print("decrypted in num : ", decrypted)

        if self.is_msg_str:
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

        return decrypted # decrypted

    def get_public_key(self):
        return self.n, self.e

    def get_private_key(self):
        return self.p, self.q, self.d
    
    def get_max_message_bits(self):
        return self.n.bit_length()

    # def __egcd(self, a, b):
    #     if a == 0:
    #         return (b, 0, 1)
    #     else:
    #         g, y, x = self.__egcd(b % a, a)
    #         return (g, x - (b // a) * y, y)

    # def __modinv(self, a, m):
    #     g, x, y = self.__egcd(a, m)
    #     if g != 1:
    #         raise Exception('modular inverse does not exist')
    #     else:
    #         return x % m


rsa = RSA()
p = 17055899557196527525682810191339089909014331959812898993437334555169285087976951946809555356817674844913188193949144165887100694620944167618997411049745043243260854998720061941490491091205087788373487296637817044103762239946752241631032791287021875863785226376406279424552454153388492970310795447866569138481
q = 171994050316145327367864378293770397343246561147593187377005295591120640129800725892235968688434055779668692095961697434700708550594137135605048681344218643671046905252163983827396726536078773766353616572531688390937410451433665914394068509329532352022301339189851111636176939179510955519440490431177444857017
rsa.generate_keys(p, q)

message = 'indriatifiqey16@gmail.com'
print("m in str : ", message)

# encrypting and decrypting
encrypted = rsa.encrypt(message, public_key=rsa.get_public_key()) 
decrypted = rsa.decrypt(encrypted, private_key=rsa.get_private_key()) 

print('---' * 40)
print("encrypted : ", encrypted)
print("decrypted in str : ", decrypted)

print('---' * 40)
if (decrypted == message):
    print("SUCCESSFULL!!!")