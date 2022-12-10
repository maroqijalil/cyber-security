import random
import math

class RSA:
    def __init__(self):
        self.e = self.d = self.p = self.q = self.phi = 0

    def __egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.__egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def __modinv(self, a, m):
        g, x, y = self.__egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def encrypt(self, m, keyPair=None):
        if (keyPair == None):
            keyPair[0] = self.e
            keyPair[1] = self.n

        return pow(m, keyPair[0], keyPair[1])

    def decrypt(self, c, keyPair=None):
        if (keyPair == None):
            keyPair[0] = self.d
            keyPair[1] = self.n

        return pow(c, keyPair[0], keyPair[1])

    def generateKeys(self, p, q, e=3):
        self.p = p
        self.q = q

        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = e
        self.d = self.__modinv(self.e, self.phi)

        if (self.phi % self.e == 0):
            raise Exception('invalid values for p and q')

    def getMaxMessageBits(self):
        return self.n.bit_length()

    def getPublicKey(self):
        return self.e, self.n

    def getPrivateKey(self):
        return self.d, self.n



rsa = RSA()
# Two 1024-bit primes
rsa.generateKeys(17055899557196527525682810191339089909014331959812898993437334555169285087976951946809555356817674844913188193949144165887100694620944167618997411049745043243260854998720061941490491091205087788373487296637817044103762239946752241631032791287021875863785226376406279424552454153388492970310795447866569138481,
                171994050316145327367864378293770397343246561147593187377005295591120640129800725892235968688434055779668692095961697434700708550594137135605048681344218643671046905252163983827396726536078773766353616572531688390937410451433665914394068509329532352022301339189851111636176939179510955519440490431177444857017)

message = 2938749823749

# Encrypting and decrypting
decrypted = rsa.decrypt(message, keyPair=rsa.getPublicKey()) #Clients use public key to encrypt and decrypt messages
encrypted = rsa.encrypt(decrypted, keyPair=rsa.getPrivateKey()) #Server uses private key to encrypt and decrypt messages

print(message)
print(encrypted)
print(decrypted)

thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

for x, v in thisdict.items():
  print(v)
  thisdict[x] = 'asd'
for x in thisdict.values():
  print(x)
