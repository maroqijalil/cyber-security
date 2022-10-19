from operation import Operation


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
