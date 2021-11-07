import socket
import ssl
import os
import threading
from datetime import datetime
from urllib.parse import unquote
CRLF = '\r\n'
ctype = {'html': 'text/html', 'htm': 'text/html', 'txt': 'text/html', 'ico': 'image/x-icon', 'css': 'text/css', 'js': 'application/javascript', 'jpg': 'image/jpeg', 'png': 'image/png', 'gif': 'image/gif', 'mp3': 'audio/mp3', 'ogg': 'audio/ogg', 'wav': 'audio/wav', 'opus': 'audio/opus', 'mp4': 'video/mp4', 'webm': 'video/webm', 'other':'application/octet-stream'}
SSL = False
def handle(sock, addr):
    try:
        request = sock.recv(2048)
        temp = request.decode().split('\r\n')
        try:
            method, path, _http = temp[0].split(' ')
        except:
            pass
        else:
            protocol, headers = _http.split('/')
            path = unquote(path)
            if os.path.exists(os.getcwd() + path):
                print(f'[{str(datetime.now()).split(".")[0]}] {addr[0]} {method} {path} 200 OK')

            elif not os.path.exists(path.split('/', 1)[1]):
                print(f'[{str(datetime.now()).split(".")[0]}] {addr[0]} {method} {path} 404 File not found')

            #print(method, path, _http)
            
            if path == '/':
                sock.send(('HTTP/1.1 200 OK' + CRLF).encode())
                sock.send((f'Content-Type: {ctype["html"]}' + CRLF * 2).encode())
                sock.send(f'<meta charset="utf-8">{CRLF}'.encode())
                if 'index.html' in os.listdir():
                    webfile = open('index.html', 'rb')
                    sock.send(webfile.read())
                    webfile.close()
    
                elif 'index.htm' in os.listdir():
                    webfile = open('index.htmf', 'rb')
                    sock.send(webfile.read())
                    webfile.close()

                else:
                    sock.send(f'<h1>Directory listing for {path}</h1>{CRLF}'.encode())
                    sock.send(f'<hr>{CRLF}'.encode())
                    sock.send(f'<ul>{CRLF}'.encode())
                    for i in os.listdir(os.getcwd() + path):
                        if os.path.isdir(os.getcwd() + path + "/" + i):
                            sock.send(f'<li><a href="{i}/">{i}</a></li>{CRLF}'.encode())
                        else:
                            sock.send(f'<li><a href="{i}">{i}</a></li>{CRLF}'.encode())
                    sock.send(f'</ul>{CRLF}'.encode())
                    sock.send(f'<hr>{CRLF}'.encode())
                    
            
            else:
                    if os.path.exists(path.split('/', 1)[1]):
                        sock.send(('HTTP/1.1 200 OK' + CRLF).encode())
                        if os.path.isfile(os.getcwd() + path):
                            ext = path.split('/', 1)[1].split('.')[-1]
                            webfile = open(path.split('/', 1)[1], 'rb')
                            if ext in ctype:
                                sock.send((f'Content-Type: {ctype[ext]}' + CRLF * 2).encode())
                                sock.send(webfile.read())
                                webfile.close()
                        
                            else:
                                sock.send((f'Content-Type: {ctype["other"]}' + CRLF * 2).encode())
                                sock.send(webfile.read())
                                webfile.close()
                        else:
                            sock.send((f'Content-Type: {ctype["html"]}' + CRLF * 2).encode())
                            sock.send(f'<meta charset="utf-8">{CRLF}'.encode())
                            if 'index.html' in os.listdir(os.getcwd() + path):
                                webfile = open(path.split('/', 1)[1] + '/index.html', 'rb')
                                sock.send(webfile.read())
                                webfile.close()
    
                            elif 'index.htm' in os.listdir(os.getcwd() + path):
                                webfile = open(path.split('/', 1)[1] + '/index.htm', 'rb')
                                sock.send(webfile.read())
                                webfile.close()
                            else:
                                sock.send(f'<h1>Directory listing for {path}</h1>{CRLF}'.encode())
                                sock.send(f'<hr>{CRLF}'.encode())
                                sock.send(f'<ul>{CRLF}'.encode())
                                for i in os.listdir(os.getcwd() + path):
                                    if os.path.isdir(os.getcwd() + path + "/" + i):
                                        sock.send(f'<li><a href="{path + "/" + i}/">{i}</a></li>{CRLF}'.encode())
                                    else:
                                        sock.send(f'<li><a href="{path + "/" + i}">{i}</a></li>{CRLF}'.encode())
                                sock.send(f'</ul>{CRLF}'.encode())
                                sock.send(f'<hr>{CRLF}'.encode())
                    
                    else:
                        sock.send(('HTTP/1.1 404 Not Found' + CRLF).encode())
                        sock.send((f'Content-Type: {ctype["html"]}' + CRLF * 2).encode())
                        sock.send(b'<h1>404 Page not found</h>')
                
                
            sock.close()
    except ConnectionResetError:
        pass
    except:
        sock.send(('HTTP/1.1 500 Internal Server Error' + CRLF).encode())
        sock.send((f'Content-Type: {ctype["html"]}' + CRLF * 2).encode())
        sock.send(b'<h1>500 Internal Server Error</h>')
        sock.close()



if __name__ == '__main__':
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if SSL:
        s = ssl.wrap_socket (s, certfile='cert.crt', keyfile='private.key', server_side=True)
        s.bind(('', 443))
    else:
        s.bind(('', 80))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.listen(0)

    while True:
        try:
            clientsock, clientaddress = s.accept()
            threading.Thread(target=handle, args=(clientsock, clientaddress)).start()
        except:
            pass

