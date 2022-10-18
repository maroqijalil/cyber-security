import math


class Binary:
    @staticmethod
    def from_hex(hex):
        return "".join(["{:04b}".format(int(i, 16)) for i in hex])

    @staticmethod
    def from_dec(dec):
        return bin(dec)[2:]

    @staticmethod
    def from_text(text):
        return "".join(format(ord(i), "08b") for i in text)

    @staticmethod
    def to_hex(bin):
        return format(int(bin, 2), 'x')

    @staticmethod
    def to_dec(binary):
        return int(binary, 2)

    @staticmethod
    def to_text(binary):
        return "".join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))

    @staticmethod
    def is_hex(text):
        try:
            int(text, 16)
            return True

        except:
            return False


class Operation:
    @staticmethod
    def permute(source, target):
        return "".join([source[i - 1] for i in target])

    @staticmethod
    def shift_left(source, n):
        return source[n:] + source[:n]

    @staticmethod
    def xor(bin_a, bin_b):
        return "".join([str(ord(a) ^ ord(b)) for a, b in zip(bin_a, bin_b)])


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


class Key:
    FIRST_COMPRESSION_PERMUTATION = \
        [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

    SHIFT_TABLE = \
        [1, 1, 2, 2,
        2, 2, 2, 2,
        1, 2, 2, 2,
        2, 2, 2, 1]

    SECOND_COMPRESSION_PERMUTATION = \
        [14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32]

    def __init__(self, key):
        self.key = Operation.permute(key, self.FIRST_COMPRESSION_PERMUTATION)
        
        self.round_keys = []
        self.__generate_round_keys()

    def __generate_round_keys(self):
        left_key = self.key[:28]
        right_key = self.key[28:]

        for i in range(0, 16):
            left_key = Operation.shift_left(left_key, self.SHIFT_TABLE[i])
            right_key = Operation.shift_left(right_key, self.SHIFT_TABLE[i])
            round_key = Operation.permute(left_key + right_key, self.SECOND_COMPRESSION_PERMUTATION)

            self.round_keys.append(round_key)
    
    def get_round_keys(self):
        return self.round_keys


class Round:
    EXPANSION_PERMUTATION = \
        [32, 1, 2, 3, 4, 5, 4, 5,
        6, 7, 8, 9, 8, 9, 10, 11,
        12, 13, 12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21, 20, 21,
        22, 23, 24, 25, 24, 25, 26, 27,
        28, 29, 28, 29, 30, 31, 32, 1]

    SBOX_TABLE = \
        [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

    PBOX_TABLE = \
        [16, 7, 20, 21,
        29, 12, 28, 17,
        1, 15, 23, 26,
        5, 18, 31, 10,
        2, 8, 24, 14,
        32, 27, 3, 9,
        19, 13, 30, 6,
        22, 11, 4, 25]

    def __init__(self, left_plain_text, right_plain_text, round_keys):
        self.left_plain_text = left_plain_text
        self.right_plain_text = right_plain_text
        self.round_keys = round_keys

        self.__process()

    def __process(self):
        for i in range(16):
            operated_right = Operation.permute(self.right_plain_text, self.EXPANSION_PERMUTATION)
            operated_right = Operation.xor(operated_right, self.round_keys[i])

            operated_right = self.__substitution(operated_right)
            operated_right = Operation.permute(operated_right, self.PBOX_TABLE)

            self.left_plain_text = Operation.xor(self.left_plain_text, operated_right)

            if (i < 15):
                self.left_plain_text, self.right_plain_text = self.right_plain_text, self.left_plain_text

    def __substitution(self, operated_right):
        result = ""
        for i in range(8):
            index = i * 6
            row = Binary.to_dec(operated_right[index] + operated_right[index + 5])
            column = Binary.to_dec(operated_right[index + 1 : index + 5])
            value = self.SBOX_TABLE[i][row][column]
            result = result + Binary.from_dec(value).zfill(4)
        
        return result
        
    def get_operated_text(self):
        return self.left_plain_text + self.right_plain_text


class DES:
    INITIAL_PERMUTATION = \
        [58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7]

    FINAL_PERMUTATION = \
        [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

    def __init__(self, plain_text, key):
        self.data = Data(plain_text)
        self.key = key

    def encrypt(self):
        round_keys = Key(self.key).get_round_keys()

        return self.__process(round_keys)

    def decrypt(self):
        round_keys = Key(self.key).get_round_keys()[::-1]

        return self.__process(round_keys)
    
    def __process(self, round_keys):
        result = ""
        for datum in self.data.get_list():
            plain_text = Operation.permute(datum, self.INITIAL_PERMUTATION)

            operated_text = Round(plain_text[:32], plain_text[32:], round_keys).get_operated_text()
            result = result + Operation.permute(operated_text, self.FINAL_PERMUTATION)
        
        return self.data.from_binary(result)


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


pt = "1234adAB8912382ashdajsdkasjd9283989hjwo8u3oik"
key = "jalilasdasjdkasdjsakjdhaksjdh9832y948hewokjhk"

print("Encryption")
cipher_text = LinearDES(pt, key).encrypt()
print("Cipher Text : ", cipher_text)

print("Decryption")
text = LinearDES(cipher_text, key).decrypt()
print("Plain Text : ", text)
