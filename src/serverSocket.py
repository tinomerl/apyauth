# Erster Test für Sockets selber erstellen
import socket

def portListener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('localhost', 1411)
    sock.bind(address)
    sock.listen(1)
    clientSocket, clientConnectionInfo = sock.accept()

    done = False

    while not done:
        port = clientSocket.recv(4096)
        clientSocket.send('i got port' + port)
        port = int(port)

        if port != 1:
            sock.bind(('0.0.0.0',port))
            continue
        else:
            done = True
    print('ClientSocket:')
    print(clientSocket)
    print('Socket Info:')
    print(clientConnectionInfo)