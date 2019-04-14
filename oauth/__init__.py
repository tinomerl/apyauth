#.....Oauth 2.0 Wrapper.....#
#.....Send credentials......#
#.......Receive Token.......#
#.....Author Tino Merl......#
#........(c) 2019...........#
#..........v0.3.............#

# A Lib for Oauth2.0 Authentication

import oauth2py.oauth.access as access
import oauth2py.oauth.refresh as refresh

class oauth(access.oauth2,refresh.refreshTkn):
    def __init__(self,app,clientid,clientsecret):
        access.oauth2.__init__(self,app,clientid,clientsecret)
        refresh.refreshTkn.__init__(self,app,clientid,clientsecret)