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
import ast
import random
import string

class oauth2:
    def __init__(self,clientid,clientsecret):
        self.clientId = clientid
        self.clientSecret = clientsecret
    
    def oauthEndpoint(self, base = '', auth = '', token = '', refresh = ''):
        self.authEndpoint = auth
        self.tokenEndpoint = token
        self.refresh = refresh
        
    def authUrlBuild(self,scope = ''):
        if len(scope) == 1 :
            self.scopes = ''.join(scope)   
        else:
            self.scopes = '%20'.join(scope)
        self.state = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(50))
        self.redirect = 'http://localhost:1410/'
        self.authUrl = self.authEndpoint + '?client_id=' + self.clientId + '&scope=' + self.scopes + '&redirect_uri=' + self.redirect + '&state=' + self.state

    def createPage(self):
        self.htmlFile='index.html'
        f=open(self.htmlFile, 'w')
        f.write("<html><body><p>Python has created this Page for the Authentication. It can now be closed.</p></body></html>")
        f.close()
        return self.htmlFile

    def portListen(self):
        self.host = 'localhost'
        self.port = 1410
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print('Started Listening')
        self.ressock, self.caddr = self.sock.accept()
        self.req = self.ressock.recv(1024)
        self.filename = self.createPage()
        self.f = open(self.filename, 'r')

        self.ressock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
        self.ressock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
        self.ressock.send(str.encode('\r\n'))
        for l in self.f.readlines():
            self.ressock.sendall(str.encode(""+l+"", 'iso-8859-1'))
            self.l = self.f.read(1024)
        self.f.close()
        self.ressock.close()
        os.unlink(self.filename)
        return self.req

    def getCode(self):
        webbrowser.open(self.authUrl)
        self.res = self.portListen()
        self.res = self.res.decode('utf-8').splitlines()
        self.res = self.res[0]
        self.res = self.res[self.res.find('?')+1:]
        self.res = self.res[:self.res.find(' ')]

        if self.res.find('?') > 0:
            print('You haven\'t written that statement yet')
        else:
            self.res = self.res[self.res.find('=')+1:self.res.find('&')]
        return self.res

    def getToken(self, method = 'post'):
        self.code = self.getCode()
        self.method = method
        if (self.method == 'post'):
            self.grantType = 'authorization_code'
            self.headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
            self.data = 'grant_type=authorization_code&client_id=' + self.clientId + '&client_secret=' + self.clientSecret + '&redirect_uri=' + self.redirect + '&code=' + self.code
            self.tokenReq = requests.post(self.tokenEndpoint, data = self.data, headers = self.headers)
        elif (self.method == 'get'):
            print(self.tokenEndpoint + '?client_id=' + self.clientId + '&redirect_uri=' + self.redirect + '&client_secret=' + self.clientSecret + '&code=' + self.code)
            self.tokenReq = requests.get(self.tokenEndpoint + '?client_id=' + self.clientId + '&redirect_uri=' + self.redirect + '&client_secret=' + self.clientSecret + '&code=' + self.code)
        
        self.token = ast.literal_eval(self.tokenReq.content)['access_token']
        return self.token
