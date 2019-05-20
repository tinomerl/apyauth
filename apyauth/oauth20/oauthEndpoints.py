class defEndpoints:
    """
    Endpoints Class that hands down the oauthEndpoints method to the other classes. 
    """
    def __init__(self):
        pass

    def oauthEndpoints(self, base = '', auth = '', token = '', refresh = ''):
        """
        This method defines the endpoints for the instance.

        Keyword Arguments:\n
        base -- placeholder
        auth -- The Authentication URL provided by the API for the Authentication Flow.
        token -- The Token URL to exchange codes and get the Tokens from.
        refresh -- The Refresh URL to exchange the refresh Token and get a new Access Token.
        """
        self.endpoints = {'base': base, 'auth': auth, 'token': token, 'refresh': refresh}
        