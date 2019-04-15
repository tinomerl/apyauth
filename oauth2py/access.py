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

class access(oauth2py.oauthEndpoints.defEndpoints):
    """
    Class for an Access Token. 

    Inherits:\n
    The oauthEndpoints method from the oauthEndpoints class.

    This class generates an AuthUrl, sends the User to an Oauth Screen, Listens to the Response on a Localhost port and exchanges the code for an access Token. Furthermore it can save the content of the Response from the tokenendpoint in a file if needed. 
    """
    def __init__(self,app,clientid,clientsecret):
        self.clientId = clientid
        self.clientSecret = clientsecret
        self.app = app
        self.state = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(50))
        self.redirect = 'http://localhost:1410/'
        oauth2py.oauthEndpoints.defEndpoints.__init__(self)
        
    def authUrlBuild(self,scope = '', additionalParams = ''):
        """
        Constructs the Authentication URL.
        
        Keyword Arguments:\n
        scope -- The scope some oauth Endpoints require to be set in the Authentication URL.\n
        additionalParams -- Extra Parameters needed for the Authentication. Needs to be defined as a dictionary.

        Returns:\n
        An URL with following parameters added:
        * Client ID
        * Client Secret
        * Scopes
        * Redirect URI
        * State Parameter
        * Response Type
        """
        if len(scope) == 1 :
            scopes = ''.join(scope)   
        else:
            scopes = '%20'.join(scope)

        extraParams = ''
        if len(additionalParams) != 0:
            for key in additionalParams:
                extraParams = extraParams + '&' + key + '=' + additionalParams[key]
        else:
            pass
        authUrl = self.endpoints['auth'] + '?client_id=' + self.clientId + '&scope=' + scopes + '&redirect_uri=' + self.redirect + '&state=' + self.state + '&response_type=code' + extraParams
        return authUrl

    def createPage(self):
        """
        Creates a simple HTML Page.

        The Page created is just to show the user that he can now return to the console.
        """
        htmlFile='index.html'
        f=open(htmlFile, 'w')
        f.write("<html><body><p>Python has created this Page for the Authentication. It can now be closed.</p></body></html>")
        f.close()
        return htmlFile

    def portListen(self):
        """
        Opens a port and Listens to Response.

        The function opens a socket on http://localhost:1410/ creates a webpage and catches the Response. When it registers an incoming session the socket is closed. It also deletes the created HTML Page.
        Returns:\n
        The received Information on the port.
        """
        host = 'localhost'
        port = 1410
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)
        print('Started Listening')
        print('Waiting for Connection on port 1410 on localhost')
        ressock, caddr = sock.accept()
        # response = sock.accept()
        # ressock = response[0]
        req = ressock.recv(1024)
        filename = self.createPage()
        f = open(filename, 'r')
        
        ressock.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
        ressock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
        ressock.send(str.encode('\r\n'))
        for i in f.readlines():
            ressock.sendall(str.encode(""+i+"", 'iso-8859-1'))
            i = f.read(1024)
        f.close()
        ressock.close()
        os.unlink(filename)
        return req

    def getCode(self,authUrl):
        """
        Calls portListen. Processes Parameters.

        Keyword Arguments:\n
        authUrl -- The Authentication URL added with Parameters.

        It reads all the parameters from the response and turns them into a dictionary. Exits if the state differs. 
       
        Returns:\n
        Code Parameter send from the authentication Server.
        """
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
        """
        Calculates the Expirydate of the Access Token.

        Keyword Arguments: \n
        respDate -- Date taken out of the Header of the Response.\n
        expiresIn -- Seconds in which the Acces Token expires in taken out of the content of the Response.

        It Adds the expiresIn to the respDate and calculates the local Time at which the Access Token will expire. 
        
        Returns:\n
        Expiry Date of Access Token (Date)
        """
        expiryDate = datetime.datetime.strptime(respDate,'%a, %d %b %Y %H:%M:%S GMT') + datetime.timedelta(seconds = expiresIn)
        fromtz =  tz.tzutc()
        totz = tz.tzlocal()
        expiryDate = datetime.datetime.strftime(expiryDate.replace(tzinfo=fromtz).astimezone(totz),'%Y-%m-%d %H:%M:%S')
        return expiryDate

    def accessToken(self, method = 'post', scope = '', additionalParams = ''):
        """
        This function gets the Access Token and saves it.

        Keyword Arguments:\n
        method -- Request method.\n
        scope -- scope needed for the Authentication.\nS
        additionalParams -- Extra Parameters needed by the Auth Server. Needs to be defined as a dictionary.

        The Function calls the authUrlBuild and overhands the constructed URL to the getCode Function to receive the code needed for the Access Token.
        Afterwards it calls the token Endpoint and exchanges the code for a token.
        It also asks you if you wanna save the token between sessions and constructs a file with the given service/app name in which the token is stored.

        Returns:\n
        Access Token from the Response
        """

        ans = input('do you wanna save between sessions? Y/N')
        authUrl = self.authUrlBuild(scope = scope, additionalParams= additionalParams)
        print(authUrl)
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