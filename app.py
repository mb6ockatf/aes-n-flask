from flask import Flask, request, render_template
from datetime import datetime as dt
from encrypt import encrypt, decrypt

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("landing.html") 


@app.route("/results", methods=['POST'])
def results():
    c_time = str(dt.now()).replace(' ', '$')
    file = request.files['selected']
    file.save(f'{c_time}')
    if request.form['crypt'] == 'encrypt':
        mode = True
    else:
        mode = False
    nonce = request.form['nonce'].encode()
    key = request.form['key'].encode()
    with open(f'{c_time}', 'rb') as stream:
        file = stream.read()
        if mode:
             result = encrypt(file, key, nonce)
        else:
            result = decrypt(file, key, nonce)
    with open(f'_{c_time}', 'wb') as file:
        file.write(result)
    return f"<p>resulti</p>"

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
