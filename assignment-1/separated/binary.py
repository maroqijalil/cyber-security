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
