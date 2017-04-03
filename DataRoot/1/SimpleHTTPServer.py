from socket import *
import _thread
import sys
import time
import os
import mimetypes
import base64

addr_arr = []
BUFF = 10000
HOST = '127.0.0.1'
PORT = 8000
root = os.getcwd()

def create_http_msg(txt):
    resp = "HTTP/1.1 200 OK\n"+\
            "Content-Length: {0}\n"+\
            "\n\n{1}"
    resp = resp.format(len(txt)+1, txt)
    return resp.encode()

def get_link(recv):
    if not recv:
        return "/"
    listStrRecv = recv.split("\n")
    head = listStrRecv[0].split(" ")
    if head[1] == "/favicon.ico":
        return "/"
    return head[1]

def create_html(listdir):
    print(root)
    html = "<html><head><meta charset='utf-8'><title='{0}'/>"+\
          "</head><body><h1>{0}</h1>{1}</body></html>"
    templateStr = "<p><a href='/files/{0}'>{0}</a></p>"
    tmpStr = ""
    for item in listdir:
        tmpStr += templateStr.format(item)
    return html.format(root, tmpStr)
    

def start():
    listdir = os.listdir()
    info = ""       
    if "index.html" in listdir:
        tmp_file = open("index.html", "r")
        info = tmp_file.read()
        tmp_file.close()
    else:
        info = create_html(listdir)
    return info

def files():
    listdir = os.listdir()
    info = create_html(listdir)
    return info

def deepFiles(way):
    res = ""
    if os.path.isfile(root+ way):
        mim = mimetypes.guess_type(root+way)
        file = open(root+way, "r")
        try:
            res = file.read()
        except Exception:
            res = "file is empty or server could not open it"
        finally:
            file.close()        
    elif os.path.isdir(root+way):
        res = create_html(os.listdir(root+way))
    if not res or res == "":
        res = "file is empty or server could not read it"
    return res
    

def handler(clientsock, addr_arr, addr):
    data = clientsock.recv(BUFF)
    recv = data.decode("utf=8")
    info = "Error"
    link = get_link(recv)
    if link == "/":
        info = start()
    elif link == "/files":
        info = files()
    elif link.find("/files/") != -1:
        info = deepFiles(link[6:])
    clientsock.send(create_http_msg(info))
    time.sleep(10)
    clientsock.close()
    addr_arr.remove(addr)
    print (addr, "- closed connection")

if __name__=='__main__':
    if len(sys.argv) > 1 and int(sys.argv[1]) > 0:
        PORT = int(sys.argv[1])
    ADDR = (HOST, PORT)
    
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    print ('waiting for connection... listening on port', PORT)    
    while 1:        
        clientsock, addr = serversock.accept()
        print ('...connected from:', addr)
        addr_arr.append(addr)
        print("\n\n"+str(addr_arr)+"\n\n")
        _thread.start_new_thread(handler, (clientsock, addr_arr, addr))
      
