#.....Oauth 2.0 Wrapper.....#
#.....Send credentials......#
#.......Receive Token.......#
#.....Author Tino Merl......#
#........(c) 2019...........#
#..........v0.3.............#

# A Lib for Oauth2.0 Authentication

import apyauth.oauth20.access as access
import apyauth.oauth20.refresh as refresh
import apyauth.oauth20.validate as validate

class oauth2(access.access, refresh.refreshTkn, validate.validateTkn):
    def __init__(self,app,clientid,clientsecret):
        access.access.__init__(self,app,clientid,clientsecret)
        refresh.refreshTkn.__init__(self,app,clientid,clientsecret)
        validate.validateTkn.__init__(self,app)