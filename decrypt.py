#!/usr/bin/python
#-*- encoding:utf-8 -*-

import os
from Cipher import Cipher

if __name__ == "__main__":
  if os.path.dirname(__file__):
      os.chdir(os.path.dirname(__file__))
  files = os.listdir()
  cipher = Cipher()
  key_file = input("Please provide the path of 'key.asc':")[1:-2]
  for i in files:
    if i.endswith(".asc") and i != "key.asc":
      encrypted_file = i
  basename = os.path.basename(encrypted_file)

  enc_path = os.path.abspath(encrypted_file)
  key_path = os.path.normpath(os.path.join(
      os.path.dirname(key_file), os.path.basename(key_file)))

  with open(enc_path, "rb") as f:
    cipher.file = f.read()
  with open(key_path, "rb") as f:
    cipher.key = f.read()
  with open(basename.rsplit(".asc")[0], "wb") as origin_file:
    origin_file.write(cipher.otp_decrypt())

  print("done.")
  exit()
