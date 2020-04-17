import os, wget
import random, string
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import shutil

def getPublicKey(ip):
    url = "http://" + str(ip) + "/static/publicKey.pub"
    filename = wget.download(url, out="Temp")

def getPassword(ip):
    try:
        shutil.rmtree("Temp")
    except:
        pass
    os.mkdir("Temp")
    getPublicKey(ip)
    N = 10
    key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
    # os.remove("Temp/publicKey")
    # print(key)
    keyF, hashKey = getPasswordEncrypted(key)
    # shutil.rmtree("Temp")
    return key, hashKey

def getPasswordEncrypted(key):
    pb_key = RSA.importKey(open('Temp/publicKey.pub', 'r').read())
    cipher = PKCS1_OAEP.new(key=pb_key)
    key = key.encode()
    ct = cipher.encrypt(key)
    return key, base64.b64encode(ct).decode()

def getKey(ciperText):
    private_key_path = "private_key.pem"
    cp = base64.decodebytes(ciperText.encode())
    pr_key = RSA.importKey(open(private_key_path, 'r').read())
    de = PKCS1_OAEP.new(key=pr_key)
    return (de.decrypt(cp)).decode()

# key, keyHash = getPassword("127.0.0.1:8000")
# print()
# print(key)
# print(keyHash)

# print(getKey(keyHash))
