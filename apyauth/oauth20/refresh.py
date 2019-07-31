import ast
import requests
import json
import os
import apyauth.oauth20.oauthEndpoints

class refreshTkn(apyauth.oauth20.oauthEndpoints.defEndpoints):
    """
    This class can be used to refresh an access Token. 

    Inherits:\n
    The oauthEndpoints method from the oauthEndpoints class.


    This class uses a refresh Token to exchange for a new Access Token. Therefore a refresh Endpoint is needed. 
    If you saved your tokens in a file you can start a new instance from the oauth class with the same app/service name you obtained the access Token with. The refreshToken method then scans the current working directory for a file corresponding to the app/service name and takes out the refresh token. If theres no file present it prompts you to paste the refresh token in the terminal.
    """
    def __init__(self,app,clientid,clientsecret):
        self.clientId = clientid
        self.clientSecret = clientsecret
        self.app = app
        apyauth.oauth20.oauthEndpoints.defEndpoints.__init__(self)

    def refreshToken(self):
        """
        This method scans the current working directory for a token file corresponding the app/service Name. If there isn't any present it asks you to paste the refresh Token into the terminal.
        Afterwards it calls the newToken method with the refresh Token and saves the response in newToken.

        Returns:\n
        A new Access Token.
        """
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
        """
        This method exchanges the refresh Token for a new Access Token.

        Keyword Arguments:\n
        refreshToken -- The refresh Token provided by the refreshToken method.

        Returns:\n
        New Access Token.
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
        data = 'grant_type=refresh_token&client_id=' + self.clientId + '&client_secret=' + self.clientSecret + '&refresh_token=' + refreshToken
        tokenReq = requests.post(self.endpoints['refresh'], data = data, headers = headers)
        token = json.loads(tokenReq.content)['access_token']
        self.tokenReq = tokenReq
        return token
