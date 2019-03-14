import threading

try: 
    from http.server import HTTPServer, SimpleHTTPRequestHandler # Python 3
except ImportError: 
    from SimpleHTTPServer import BaseHTTPServer
    HTTPServer = BaseHTTPServer.HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler # Python 2

server = HTTPServer(('', 1410), SimpleHTTPRequestHandler)
thread = threading.Thread(target = server.serve_forever)
thread.daemon = True
thread.start()

def fin():
    server.shutdown()

print('server running on port {}'.format(server.server_port))