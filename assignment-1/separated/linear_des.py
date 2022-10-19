from des import DES
from data import Data


class LinearDES:
    def __init__(self, plain_text, key):
        self.keys = Data(key).get_list()
        self.data = plain_text

    def encrypt(self):
        result = self.data
        for key in self.keys:
            result = DES(result, key).encrypt()
        
        return result

    def decrypt(self):
        result = self.data
        for key in self.keys[::-1]:
            result = DES(result, key).decrypt()
        
        return result
