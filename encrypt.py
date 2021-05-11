#!/usr/bin/python
from Cipher import Cipher
import os

if __name__ == "__main__":
  cipher = Cipher()
  path = input(
      "Please create a zip archive of your files and provide the path:").strip()[1:-1]
  dirname = os.path.dirname(path)
  basename = os.path.basename(path)
  path = os.path.normpath(os.path.join(dirname, basename))

  with open(path, "rb") as f:
    cipher.file = f.read()
    cipher.length = len(cipher.file)
    cipher.generate_key()

    with open("%s.asc" %(basename), "wb") as encrypted_file:
      encrypted_file.write(cipher.otp_encrypt())
    with open("key.asc", "wb") as key_file:
      key_file.write(cipher.key)
      
  print("done.")
  exit()
