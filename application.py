import os
from flask import Flask, request, render_template, flash, url_for, send_from_directory, redirect, send_file
from s3_function import list_files, download_file, upload_file
import pyqrcode
import io
import base64
import sqlite3
import html

app = Flask(__name__)
app.secret_key = "key123"
DOWNLOAD_CODE = "Codes"
BUCKET = "qrgenerator-code"
processed_text=''


@app.route('/')
def index():
    contents = list_files("qrgenerator-code")
    return render_template("base.html", contents=contents)


@app.route('/qrgenerated', methods= ['POST'])
def textfield():
    global processed_text
    processed_text = request.form['text']
    global filename
    filename=processed_text
    if processed_text == '':
        flash("Please enter a value!")
        contents = list_files("qrgenerator-code")
    else:
        QR(filename)
        upload_file(f"{filename}.png", BUCKET)
        contents = list_files("qrgenerator-code")
        flash("Your QR code has been generated!")
    return render_template("base.html", contents=contents)

def QR(filename):
#    connection = sqlite3.connect('inviteeslist.db')
    QR = pyqrcode.create(filename)
    QR.png(f'{filename}.png', scale=8)

#    connection.execute(f"INSERT OR REPLACE INTO (CODE,NAME) VALUES ('x','x')")
    return filename

@app.route(f'/code')
def getCode(filename):
    return send_from_directory('Codes',filename)

@app.route(f"/download", methods=['GET'])
def download():
    if request.method == 'GET':
        output = download_file('www.google.com.png', BUCKET)

        return send_file(output, as_attachment=True)


# @app.route('/QR', methods= ['GET'])
# def QRimage():
#      global processed_text
#      im = Image.open(f'Codes/{processed_text}.png')
#      data = io.BytesIO()
#      im.save(data, "PNG")
#      encoded_img_data = base64.b64encode(data.getvalue())
#      img_data = encoded_img_data.decode('utf-8')
#      return render_template('base.html', value = img_data)


if __name__ == '__main__':
    app.run(debug= True)
