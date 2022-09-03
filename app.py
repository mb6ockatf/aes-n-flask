from os import mkdir, remove, chmod, rmdir
from sys import argv
from datetime import datetime as dt
from shutil import make_archive
from flask import Flask, request, render_template, send_file, flash, redirect, session, url_for
from werkzeug.exceptions import HTTPException
from Crypto.Cipher import AES
from stat import S_IWRITE
from shutil import rmtree


def encrypt(data: bytes, key: bytes):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext = cipher.encrypt(data)
    return ciphertext, cipher.nonce


def decrypt(ciphertext: bytes, key: bytes, nonce: bytes):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


app = Flask(__name__)
# app.secret_key = argv[1].encode()
app.secret_key = "bhfsuidbsbndisbds"
app.permanent_session_lifetime = False


"""@app.route("/favicon.ico")
def favicon():
    return redirect(url_for('avicon.ico'))"""


@app.route("/")
def main():
    return render_template("landing.html")


@app.route("/crypto_form_handler", methods=["GET", "POST"])
def crypto_form_handler():
    c_time = str(dt.now()).replace(' ', '-').replace(':', '-')
    mkdir(str(c_time))
    uploaded_path = f"{c_time}/uploaded.bin"
    nonce_path = f"{c_time}/nonce.bin"
    result_path = f"{c_time}/result.bin"
    file = request.files['selected']
    file.save(uploaded_path)
    file = open(uploaded_path, 'rb')
    file_contents = file.read()
    key = request.form['key'].encode()
    mode = request.form['crypt']
    if mode == 'encrypt':
        result, nonce = encrypt(file_contents, key)
        with open(nonce_path, "wb") as opened:
            opened.write(nonce)
        with open(result_path, "wb") as opened:
            opened.write(result)
        result = send_file(make_archive("encrypted", "tar", str(c_time)))
    elif mode == 'decrypt':
        nonce = request.files["nonce"]
        nonce.save(nonce_path)
        with open(nonce_path, "rb") as stream:
            nonce = stream.read()
        result = decrypt(file_contents, key, nonce)
        with open(result_path, "wb") as file:
            file.write(result)
        result = send_file(result_path)
    else:
        flash('Режим не выбран')
        result = redirect(request.url)
    file.close()
    chmod(c_time, S_IWRITE)
    rmtree(c_time, ignore_errors=True)
    return result


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
    serve(app, host="127.0.0.1", port=8080)
