import socket

HOST = ''   # use '' to expose to all networks
PORT = 1410

def incoming(host, port):
  """Open specified port and return file-like object"""
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # set SOL_SOCKET.SO_REUSEADDR=1 to reuse the socket if
  # needed later without waiting for timeout (after it is
  # closed, for example)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((host, port))
  sock.listen(0)   # do not queue connections
  request, addr = sock.accept()
  ## With this little Piece of Code you got what you needed
  # sock.send("Some String")
  answer = request.recv(1024)

  file = open("index.html", 'r')
  sock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
  sock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
  sock.send(str.encode('\r\n'))

  for l in file.readlines():
    print('Sent ', repr(l))
    sock.sendall(str.encode(""+l+"", 'iso-8859-1'))
    l = f.read(1024)
    
  return answer

var = incoming(HOST, PORT)
