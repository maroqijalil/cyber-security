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
