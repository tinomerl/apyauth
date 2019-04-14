import oauth2py.access as access
import oauth2py.refresh as refresh

class oauth(access.oauth2,refresh.refreshTkn):
    def __init__(self,app,clientid,clientsecret):
        access.oauth2.__init__(self,app,clientid,clientsecret)
        refresh.refreshTkn.__init__(self,app,clientid,clientsecret)