import oauth2py.core as oauth2py

class initSessiosn(oauth2py.oauth2):
    def __init__(self,clientid,clientsecret):
        oauth2py.oauth2.__init__(self,clientid,clientsecret)