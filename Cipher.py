#!/usr/bin/python
import secrets
import os

class Cipher:
  def __init__(self):
    self.key    = None
    self.file   = None
    self.length = 0

  def generate_key(self):
    self.key = secrets.token_bytes(self.length)

  def otp_encrypt(self):
    key = self.key
    return bytes([key[i] ^ self.file[i] for i in range(len(self.file))])
    
  def otp_decrypt(self):
    key = self.key
    return bytes([key[i] ^ self.file[i] for i in range(len(self.file))])



