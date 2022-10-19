from linear_des import LinearDES


if __name__ == "__main__":
    plain_text = "1234adAB891238klashkdakskjdk2"
    key = "jalilas"

    print("Encryption")
    cipher_text = LinearDES(plain_text, key).encrypt()
    print("Cipher Text : ", cipher_text)

    print("Decryption")
    text = LinearDES(cipher_text, key).decrypt()[:len(plain_text)]
    print("Plain Text : ", text)
