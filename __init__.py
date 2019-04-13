import oauth2py.core as oauth2py

class initSession(oauth2py.oauth2):
    def __init__(self,app,clientid,clientsecret):
        oauth2py.oauth2.__init__(self,app,clientid,clientsecret)