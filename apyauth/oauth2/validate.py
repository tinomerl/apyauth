import ast
import datetime

class validateTkn:
    """
    This Class validates your saved Access Token and checks the expiry Date if you have a token saved locally.
    """
    def __init__(self,app):
        self.app = app
    
    def validate(self):
        """
        Method that validates the Access token.

        It checks if there is any token in the current working directory for the given service Name. If there is one to be found it checks the saved expiry Date with the current Sysdate.

        Returns:\n
        Tuple.
        Access or Refresh Token. Depending on the Expiry Date and if theres one present. If there is no Access or Refresh Token present the first value of the tuple will let you know.
        Boolean that determines the current state of the Access Token. True if it is still valid. False if not and if there isn't any token.
        """
        try:
            f = open(('.' + self.app + '-token'), 'r')
            tokenDict = ast.literal_eval(f.read())
            f.close()
            expiryDate = tokenDict['expiryDate']
            expiryDateTime = datetime.datetime.strptime(expiryDate, '%Y-%m-%d %H:%M:%S')
            sysTime = datetime.datetime.now()

            if expiryDateTime <= sysTime:
                print('Access Token has expired. Reauthenticate or use a refresh Token')
                try:
                    return tokenDict['refresh_token'], False
                except:
                    return 'NoRefreshTokenFound', False
            elif expiryDateTime >= sysTime:
                print('Access Token is still valid until ' + expiryDate)
                return tokenDict['access_token'], True
        except:
            print('No token or expiry Date found for ' + self.app + ' in the current environment.')
            return 'NoAccessTokenFound', False
