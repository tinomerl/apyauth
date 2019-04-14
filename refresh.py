import ast
import requests
import json
import os
import oauth2py.oauthEndpoints

class refreshTkn(oauth2py.oauthEndpoints.defEndpoints):
    def __init__(self,app,clientid,clientsecret):
        self.clientId = clientid
        self.clientSecret = clientsecret
        self.app = app
        oauth2py.oauthEndpoints.defEndpoints.__init__(self)

    def refreshToken(self):
        try:
            f = open(('.' + self.app + '-token'), 'r')
            refreshToken = ast.literal_eval(f.read())['refresh_token']
        except:
            try:
                refreshToken = self.tokenReq['refresh_token']
            except:
                print('No Refresh Token Found in current Environment. Please paste it here:')
                refreshToken = input()
        newToken = self.newToken(refreshToken)
        return(newToken)
    
    def newToken(self,refreshToken):
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
        data = 'grant_type=refresh_token&client_id=' + self.clientId + '&client_secret=' + self.clientSecret + '&refresh_token=' + refreshToken
        tokenReq = requests.post(self.endpoints['refresh'], data = data, headers = headers)
        token = json.loads(tokenReq.content)['access_token']
        self.tokenReq = tokenReq
        return token