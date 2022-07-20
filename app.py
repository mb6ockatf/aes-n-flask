from os import path, mkdir, remove
from sys import argv
from datetime import datetime as dt
from base64 import encodebytes
from shutil import make_archive
from flask import Flask, request, render_template, send_file, flash, redirect, session, url_for
from werkzeug.exceptions import HTTPException
from Crypto.Cipher import AES


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


@app.route("/favicon.ico")
def favicon():
    return redirect(url_for('static'), filename='favicon.ico')


@app.route("/")
def main():
    return render_template("landing.html")


@app.route("/crypto_form_handler", methods=["GET", "POST"])
def crypto_form_handler():
    c_time = str(dt.now()).replace(' ', '-')
    mkdir(c_time, mode=0o777)
    uploaded_path = f"{c_time}/uploaded.bin"
    nonce_path = f"{c_time}/nonce.bin"
    result_path = f"{c_time}/result.bin"
    encrypted_archieve = f"{c_time}/encrypted.tar"
    file = request.files['selected'].save(uploaded_path)
    file = open(uploaded_path, 'rb').read()
    key = request.form['key'].encode()
    mode = request.form['crypt']
    if mode == 'encrypt':
         result, nonce = encrypt(file, key)
         with open(nonce_path, "wb") as file:
             file.write(nonce)
         with open(result_path, "wb") as file:
             file.write(result)
         return send_file(make_archive("encrypted", "tar", c_time))
    elif mode == 'decrypt':
        nonce = request.files["nonce"].save(nonce_path)
        with open(nonce_path, "rb") as stream:
            nonce = stream.read()
        result = decrypt(file, key, nonce)
        with open(result_path, "wb") as file:
            file.write(result)
        return send_file(result_path)
    else:
        flash('Режим не выбран')
        return redirect(request.url)
    file.close()
    remove(c_time)


@app.route("/keys_form_handler", methods=["GET", "POST"])
def keys_from_handler():
    key = request.form['key'].encode()
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    print(nonce.decode())


@app.errorhandler(HTTPException)
def http_error_handler(error):
    return render_template("error.html", error=error), error.code


@app.errorhandler(Exception)
def other_error_handler(error):
    return render_template("error.html", error=error)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

