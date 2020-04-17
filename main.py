from httpServer.app import main
from multiprocessing import Process
from fileHandling.fileH import addFileUI
import time, requests
import os, socket, psutil
flask_process = Process(target=main)
flask_process.start()
# flask_process.terminate()
import secureED as sed
import Encyption as en
import sys, wget

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def StartStuff():
    time.sleep(1)
    os.system("clear")
    try:
        os.mkdir("Downloads")
    except:
        pass

def addOption():
    addFileUI()

# def searchAllOtheUser():
#     ipPort = str(input("Enter Ip And Port: "))
#     response = requests.get(url="http://" + ipPort + "/files")
#     print(response.json())


def get_ip_addresses(family):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == family:
                yield (interface, snic.address)

def getListIPv4():
    ipv4s = list(get_ip_addresses(socket.AF_INET))
    ll = []
    for i in ipv4s:
        ll.append(i[1])
    return ll

def searchAllOtheUser():
    os.system("clear")
    print("Select Below LAN : ")
    ll = getListIPv4()
    z = 1
    for i in ll:
        print(str(z)  + ") " + str(i) )
        z = z +  1
    val = input(":")
    ip = ll[int(val)-1]
    users = []
    for port in range(8000, 8020):
        progress(port-8000+1, 9001-8000, status='Finding Users')
        try:
            res = requests.get(url="http://" + ip + ":" + str(port) + "/check")
            out = res.json()
            if out["check"] == 1:
                users.append(str(ip + ":" + str(port)))
        except Exception as e :
            # print(e)
            pass
    # print(users)
    os.system("clear")
    print("Select one of The Users")
    zz = 1
    for i in users:
        print(str(zz) + ") " + i)
        zz = zz + 1
    val = input(":")
    user = users[int(val)-1]
    res = requests.get(url="http://" + user + "/files")
    fileList = res.json()
    print("Select one of The File")
    zz = 1
    for i in fileList:
        print(str(zz) + ") " + i)
        zz = zz + 1
    val = input(":")
    filename = fileList[int(val)-1]
    print("downloading", filename)
    key, keyHash = en.getPassword(user)
    print(key)
    readyURL = "http://" + str(user) + "/readyFile"
    out = {"filename" : filename, "keyHash" : keyHash}
    import json
    out = json.dumps(out)
    readyRES = requests.post(readyURL, json=out)
    res = readyRES.json()
    filename = res["Name"]
    url = "http://" + str(user) + "/getFile/" + str(filename)
    filename = wget.download(url, out="Downloads")
    print("\nFile Downloaded")
    out_files = filename[:-4]
    # print(key)
    sed.decrypt_file(key=key, in_filename=filename, out_filename=out_files)
    time.sleep(1)


StartStuff()
while True:
    os.system("clear")
    num = str(input("Select A option \n1) Add File\n2) Get File \n3) Quit\n :"))
    if num == "1":
        addFileUI()
    elif num == "2":
        searchAllOtheUser()
    else:
        flask_process.terminate()
        break