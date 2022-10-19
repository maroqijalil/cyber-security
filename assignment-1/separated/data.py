
import math
from binary import Binary


class Data:
    def __init__(self, plain_text):
        self.block_size = 16 if Binary.is_hex(plain_text) else 8
        self.data = plain_text.ljust(math.ceil(len(plain_text) / self.block_size) * self.block_size, "0")

    def to_binary(self, data):
        if (self.block_size == 16):
            return Binary.from_hex(data)
        
        else:
            return Binary.from_text(data)

    def from_binary(self, data):
        if (self.block_size == 16):
            return Binary.to_hex(data)
        
        else:
            return Binary.to_text(data)
    
    def get_list(self):
        return [self.to_binary(self.data[i:i + self.block_size]) for i in range(0, len(self.data), self.block_size)]
