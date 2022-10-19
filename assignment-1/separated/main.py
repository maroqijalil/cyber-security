from linear_des import LinearDES


if __name__ == "__main__":
    plain_text = "DEMO dilakukan pada jam yang sudah tertera melalui link google meet yang akan dikirim lewat ketua kelas atau akan langsung saya taruh disini ketika demo akan segera mulai."
    key = "921839812u39218he812he189heh290812hre9238hr298"

    print("Encryption")
    cipher_text = LinearDES(plain_text, key).encrypt()
    print("Cipher Text : ", cipher_text)

    print("Decryption")
    text = LinearDES(cipher_text, key).decrypt()[:len(plain_text)]
    print("Plain Text : ", text)
