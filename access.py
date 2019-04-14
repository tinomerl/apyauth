import webbrowser
import os
import socket
import requests
import json
import random
import string
import datetime
from dateutil import tz
import oauth2py.oauthEndpoints

class oauth2(oauth2py.oauthEndpoints.defEndpoints):
    def __init__(self,app,clientid,clientsecret):
        self.clientId = clientid
        self.clientSecret = clientsecret
        self.app = app
        self.state = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(50))
        self.redirect = 'http://localhost:1410/'
        oauth2py.oauthEndpoints.defEndpoints.__init__(self)
        
    def authUrlBuild(self,scope = ''):
        if len(scope) == 1 :
            scopes = ''.join(scope)   
        else:
            scopes = '%20'.join(scope)
        authUrl = self.endpoints['auth'] + '?client_id=' + self.clientId + '&scope=' + scopes + '&redirect_uri=' + self.redirect + '&state=' + self.state + '&response_type=code'
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
        params = res[res.find('?')+1:res.find('HTTP')-1]
        paramsList = params.split('&')
        paramsDict = {}
        for i in paramsList:
            key, val = i.split('=')
            paramsDict.update({key: val})

        state = paramsDict['state']
        if self.state != state:
            print('SessionError')
            exit()
        else:
            pass
        code = paramsDict['code']
        return code

    def calcExpiryDate(self,respDate, expiresIn):
        expiryDate = datetime.datetime.strptime(respDate,'%a, %d %b %Y %H:%M:%S GMT') + datetime.timedelta(seconds = expiresIn)
        fromtz =  tz.tzutc()
        totz = tz.tzlocal()
        expiryDate = datetime.datetime.strftime(expiryDate.replace(tzinfo=fromtz).astimezone(totz),'%Y-%m-%d %H:%M:%S')
        return expiryDate

    def accessToken(self, method = 'post', scope = ''):
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
        
        headers = tokenReq.headers
        tokens = json.loads(tokenReq.content)
        expiryDate = self.calcExpiryDate(headers['Date'],tokens['expires_in'])
        tokens.update({'expiryDate': expiryDate})

        if ans.upper() == 'Y':
            f = open(('.' + self.app + '-token'), 'w+')
            f.write(str(tokens))
            f.close
        else:
            pass
        
        accToken = tokens['access_token']
        
        return accToken