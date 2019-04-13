#.....Oauth 2.0 Wrapper.....#
#.....Send credentials......#
#.......Receive Token.......#
#.....Author Tino Merl......#
#........(c) 2019...........#
#..........v0.1.............#

# A Class for Oauth2.0 Authentication
import webbrowser
import os
import socket
import requests
import json
import random
import string

class oauth2:
    def __init__(self,app,clientid,clientsecret):
        self.clientId = clientid
        self.clientSecret = clientsecret
        self.app = app
        self.state = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(50))
        self.redirect = 'http://localhost:1410/'
    
    def oauthEndpoint(self, base = '', auth = '', token = '', refresh = ''):
        endpoints = {'base': base, 'auth': auth, 'token': token, 'refresh': refresh}
        self.endpoints = endpoints
        
    def authUrlBuild(self,scope = ''):
        if len(scope) == 1 :
            scopes = ''.join(scope)   
        else:
            scopes = '%20'.join(scope)
        authUrl = self.endpoints['auth'] + '?client_id=' + self.clientId + '&scope=' + scopes + '&redirect_uri=' + self.redirect + '&state=' + self.state
        return authUrl

    def createPage(self):
        htmlFile='index.html'
        f=open(htmlFile, 'w')
        f.write("<html><body><p>Python has created this Page for the Authentication. It can now be closed.</p></body></html>")
        f.close()
        return htmlFile

    def portListen(self):
        host = 'localhost'
        port = 1410
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)
        print('Started Listening')
        print('Waiting for Connection on port 1410 on localhost')
        ressock, caddr = sock.accept()
        req = ressock.recv(1024)
        filename = self.createPage()
        f = open(filename, 'r')
        ressock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
        ressock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
        ressock.send(str.encode('\r\n'))
        for l in f.readlines():
            ressock.sendall(str.encode(""+l+"", 'iso-8859-1'))
            l = f.read(1024)
        f.close()
        ressock.close()
        os.unlink(filename)
        return req

    def getCode(self,authUrl):
        webbrowser.open(authUrl)
        res = self.portListen()
        res = res.decode('utf-8').splitlines()
        res = res[0]
        state = res[res.find('state=')+6:res.find('HTTP')-1]
        if self.state != state:
            print('SessionError')
            exit()
        else:
            pass

        code = res[res.find('code=')+5:]
        code = code[:code.find('&')]
        return code

    def getToken(self, method = 'post', scope = ''):
        ans = input('do you wanna save between sessions? Y/N')
        authUrl = self.authUrlBuild(scope = scope)
        code = self.getCode(authUrl)
        if (method == 'post'):
            headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
            data = 'grant_type=authorization_code&client_id=' + self.clientId + '&client_secret=' + self.clientSecret + '&redirect_uri=' + self.redirect + '&code=' + code
            tokenReq = requests.post(self.endpoints['token'], data = data, headers = headers)
        elif (method == 'get'):
            print(self.endpoints['token'] + '?client_id=' + self.clientId + '&redirect_uri=' + self.redirect + '&client_secret=' + self.clientSecret + '&code=' + code)
            tokenReq = requests.get(self.endpoints['token'] + '?client_id=' + self.clientId + '&redirect_uri=' + self.redirect + '&client_secret=' + self.clientSecret + '&code=' + code)
        
        if ans.upper() == 'Y':
            f = open(('.' + self.app + '-token'), 'w+')
            f.write(str(json.loads(tokenReq.content)))
            f.close
        else:
            pass

        token = json.loads(tokenReq.content)['access_token']
        return token