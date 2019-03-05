import socket

HOST = 'localhost'   # use '' to expose to all networks
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

  ## Try it tomorrow again with recv or sendall eins von den beiden
  return request.makefile('r', 0)

for line in incoming(HOST, PORT):
  print(line),
  var = (line),