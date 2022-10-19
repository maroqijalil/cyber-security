from linear_des import LinearDES


if __name__ == "__main__":
  plain_text = "1234adAB8912382ashdajsdkasjd9283989hjwo8u3oik1231"
  key = "jalilasdasjdkasdjsakjdhaksjdh9832y948hewokjhk"

  print("Encryption")
  cipher_text = LinearDES(plain_text, key).encrypt()
  print("Cipher Text : ", cipher_text)

  print("Decryption")
  text = LinearDES(cipher_text, key).decrypt()
  print("Plain Text : ", text)
