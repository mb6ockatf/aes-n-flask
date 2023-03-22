"""Encryption class"""
from Crypto.Cipher import AES


class Encryption:

    @staticmethod
    def encrypt(data: bytes, key: bytes):
        cipher = AES.new(key, AES.MODE_EAX)
        cipher_text = cipher.encrypt(data)
        return cipher_text, cipher.nonce

    @staticmethod
    def decrypt(ciphertext: bytes, key: bytes, nonce: bytes):
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext
