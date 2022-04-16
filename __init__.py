import os
import boto3


os.environ['AWS_PROFILE'] = "Profile1"
os.environ['AWS_DEFAULT_REGION'] = "us-east-1"

from flask import Flask, request, render_template, flash, url_for, send_from_directory, redirect, send_file
import pyqrcode
import io
import base64
import sqlite3
import html
import os

global bucket
app = Flask(__name__)
app.secret_key = ""
DOWNLOAD_CODE = "Codes"
BUCKET = "qrgenerator-code"
processed_text=''


def upload_file(filename: object, bucket: object) -> object:
    object_name = (f'{filename}')
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(filename, bucket, object_name)

    return response

def download_file(filename, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = filename
    s3.Bucket(bucket).download_file(filename, output)

    return output

def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents

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
    QR = pyqrcode.create(filename)
    QR.png(f'{filename}.png', scale=8)
    return filename

@app.route(f'/code')
def getCode(filename):
    return send_from_directory('Codes',filename)

@app.route(f"/download", methods=['GET'])
def download():
    if request.method == 'GET':
        output = download_file('www.google.com.png', BUCKET)

        return send_file(output, as_attachment=False)


if __name__ == '__main__':
    app.run(debug= True)
