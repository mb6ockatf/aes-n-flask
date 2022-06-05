from Crypto.Cipher import AES

def encrypt(data: bytes, key: bytes, nonce: bytes):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    ciphertext = cipher.encrypt(data)
    return ciphertext


def decrypt(ciphertext: bytes, key: bytes, nonce: bytes):
   cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
   plaintext = cipher.decrypt(ciphertext)
   return plaintext

"""
data = 'текстекстекст'
key = '1234567890`12345'
cpt, nonce, key = encrypt(data, key)

print('cpt:', cpt, '\n', 'nonce:', nonce, '\n', 'key:', key)
print()
plaintext, nonce, key = decrypt(cpt, nonce, key)
print('plt:', plaintext.decode(), '\n', 'nonce:', nonce, '\n', 'key:', key)
"""

