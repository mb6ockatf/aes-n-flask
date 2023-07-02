#!/usr/bin/env python3
import os
import sys
from datetime import datetime as dt
from shutil import make_archive, rmtree
from stat import S_IWRITE
from flask import Flask, request, render_template, send_file, redirect, url_for
from werkzeug.exceptions import HTTPException
from Crypto.Cipher import AES
from crypt_lib import Encryption


def get_safe_time() -> str:
	time = str(dt.now())
	time = time.replace(" ", "-")
	time.replace(":", "-")
	return time


app = Flask(__name__)
app.secret_key = sys.argv[1].encode()
app.permanent_session_lifetime = False


@app.route("/favicon.ico")
def favicon():
	return redirect(url_for("static", filename='favicon.ico'))


@app.route("/")
def main():
	return render_template("landing.html")


@app.route("/crypto_form_handler", methods=["GET", "POST"])
def crypto_form_handler():
	c_time = get_safe_time()
	os.mkdir(str(c_time))
	uploaded_path = c_time + os.sep + "uploaded.bin"
	nonce_path = c_time + os.sep + "nonce.bin"
	result_path = c_time + os.sep + "result.bin"
	file = request.files['selected']
	file.save(uploaded_path)
	file = open(uploaded_path, 'rb')
	file_contents = file.read()
	key = request.form['key'].encode()
	mode = request.form['crypt']
	match mode:
		case 'encrypt':
			result, nonce = Encryption.encrypt(file_contents, key)
			with open(nonce_path, "wb") as opened:
				opened.write(nonce)
			with open(result_path, "wb") as opened:
				opened.write(result)
			result = send_file(make_archive("encrypted", "tar", str(c_time)))
		case 'decrypt':
			nonce = request.files["nonce"]
			nonce.save(nonce_path)
			with open(nonce_path, "rb") as stream:
				nonce = stream.read()
			result = Encryption.decrypt(file_contents, key, nonce)
			with open(result_path, "wb") as file:
				file.write(result)
			result_path = ".." + os.sep + result_path
			result = send_file(result_path)
	file.close()
	print(os.listdir("."))
	os.chmod(c_time, S_IWRITE)
	rmtree(c_time, ignore_errors=False)
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
	serve(app, host="127.0.0.1", port=80)
