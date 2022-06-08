from flask import Flask, request, render_template, send_file, flash, redirect, session
from datetime import datetime as dt
from Crypto.Cipher import AES
from werkzeug.exceptions import HTTPException
import os
from shutil import make_archive
from sys import argv
from base64 import encodebytes

def encrypt(data: bytes, key: bytes):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext = cipher.encrypt(data)
    return ciphertext, cipher.nonce


def decrypt(ciphertext: bytes, key: bytes, nonce: bytes):
   cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
   plaintext = cipher.decrypt(ciphertext)
   return plaintext



app = Flask(__name__)
app.secret_key = argv[1].encode()
app.permanent_session_lifetime = False


@app.route("/")
def main():
    return render_template("landing.html") 

@app.route("/crypto_form_handler", methods=["GET", "POST"])
def crypto_form_handler():
    c_time = str(dt.now()).replace(' ', '$')
    try:
        file = request.files['selected']
    except KeyError:
        raise
    if file.filename == '':
        flash('Файл не загружен')
        return redirect(request.url)
    os.mkdir(c_time, mode=0o777)
    file.save(os.path.join(c_time, 'uploaded.bin'))
    key = request.form['key'].encode()
    file = open(os.path.join(c_time, 'uploaded.bin'), 'rb').read()
    if request.form['crypt'] == 'encrypt':
         os.mkdir(os.path.join(c_time, "result"), mode=0o777)
         result, nonce = encrypt(file, key)
         with open(os.path.join(c_time, "result", "nonce.bin"), "wb") as file:
             file.write(nonce)
         with open(os.path.join(c_time, "result", "result.bin"), "wb") as file:
             file.write(result)
         make_archive(os.path.join(c_time, "encrypted"), 'tar',
             os.path.join(c_time, "result"))
         return send_file(os.path.join(c_time, "encrypted.tar"))
    elif request.form['crypt'] == 'decrypt':
        nonce = request.files["nonce"].save(os.path.join(c_time, "nonce.bin"))
        with open(os.path.join(c_time, "nonce.bin"), "rb") as stream:
            nonce = stream.read()
        result = decrypt(file, key, nonce)
        with open(os.path.join(c_time, "result.bin"), "wb") as file:
            file.write(result)
        return send_file(os.path.join(c_time, "result.bin"))
    else:
        print(1)
        flash('Режим не выбран')
        return redirect(request.url)


@app.route("/keys")
def keys():
    return render_template("keys.html")


@app.route("/keys_form_handler", methods=["GET", "POST"])
def keys_from_handler():
    key = request.form['key'].encode()
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    print(nonce.decode())

"""
@app.errorhandler(HTTPException)
def http_error_handler(error):
    return render_template("error.html", error=error), error.code


@app.errorhandler(Exception)
def other_error_handler(error):
    return render_template("error.html", error=error)
"""
app.run(debug=True)
"""
public, private = newkeys(512)
message = 'Hello, world'.encode('utf8')
print("The text in utf8 is:", message)
crypto = encrypt(message, public)
print("Crypto is", crypto)
message = decrypt(crypto, private).decode('utf8')
print("Decrypted message is", message)
"""
