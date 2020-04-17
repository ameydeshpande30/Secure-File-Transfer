from flask import Flask, jsonify, send_from_directory, abort, request
from fileHandling.fileH import getFiles
from fileHandling.db import getAllFilesPath
import shutil, os
import secureED as sed
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import sampleKey
app = Flask(__name__)


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
try:
    os.mkdir("Share")
except:
    pass

def fileCopy(filename):
    path = ''
    ll = getAllFilesPath()
    for i in ll:
        if i["name"] == filename:
            path = i["path"]
            break
    source = path
    destination = "Share/" + filename
    dest = shutil.copyfile(source, destination) 

def getKey(ciperText):
    private_key_path = "private_key.pem"
    cp = base64.decodebytes(ciperText.encode())
    pr_key = RSA.importKey(open(private_key_path, 'r').read())
    de = PKCS1_OAEP.new(key=pr_key)
    return (de.decrypt(cp)).decode()

def FileEncrpt(filename, keyHash):
    fileCopy(filename)
    key = getKey(keyHash)
    # print(key, "Server --------")
    source = "Share/" + filename
    sed.encrypt_file(key, source)
    os.remove("Share/" + filename)
    return filename + ".aes"


@app.route("/files")
def getFilesList():
    return jsonify(getFiles())
    
@app.route("/check")
def check():
    return jsonify({"check": 1})

@app.route("/readyFile", methods=["POST"])
def readyFile():
    content = request.get_json(silent=True)
    # print(content)
    import json
    content = json.loads(content)
    keyHash = content["keyHash"]
    fileName = content["filename"]
    # print(fileName)
    name = FileEncrpt(fileName, keyHash)
    return jsonify({"Name" : name})

@app.route("/getFile/<string:fileName>")
def get_FIle(fileName):
    try:
        path = os.path.abspath("Share")
        # print(path, fileName)
        return send_from_directory(path, filename=fileName, as_attachment=True)
    except FileNotFoundError:
        abort(404)



@app.route("/getFileBac/<string:fileName>")
def get_image(fileName):
    try:
        path = ''
        ll = getAllFilesPath()
        for i in ll:
            if i["name"] == fileName:
                path = i["path"]
                break
        ll = path.split("/")
        ll = ll[:-1]
        lastPath = ""
        for i in ll:
            lastPath += i  + "/"
        lastPath = lastPath[:-1] 
        print(lastPath)
        return send_from_directory(lastPath, filename=fileName, as_attachment=True)
    except FileNotFoundError:
        abort(404)

def main():
    global app
    app.run(port=8000, host="0.0.0.0")