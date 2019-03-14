import socket
import os

# Standard socket stuff:
host = ''
port = 1410

def createPage():
    htmlFile='index.html'
    f=open(htmlFile, 'w')
    f.write("<html><body><p>Python has created this Page for the API Call. It can now be closed.</p></body></html>")
    f.close()
    return htmlFile

# Loop forever, listening for requests:
def incoming(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5) 
    csock, caddr = sock.accept()
    print("Connection from: " + str(caddr))
    req = csock.recv(1024)  # get the request, 1kB max
    # Look in the first line of the request for a move command
    # A move command should be e.g. 'http://server/move?a=90'
    filename = createPage()
    f = open(filename, 'r')

    csock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
    csock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
    csock.send(str.encode('\r\n'))
    # send data per line
    for l in f.readlines():
        print('Sent ', repr(l))
        csock.sendall(str.encode(""+l+"", 'iso-8859-1'))
        l = f.read(1024)
    f.close()
    csock.close()
    os.unlink(filename)
    return req

var = incoming('', 1410)
newvar = var.decode("UTF-8").splitlines()
newvar[0]