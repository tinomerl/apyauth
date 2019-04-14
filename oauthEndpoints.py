class defEndpoints:
    def __init__(self):
        pass

    def oauthEndpoints(self, base = '', auth = '', token = '', refresh = ''):
        self.endpoints = {'base': base, 'auth': auth, 'token': token, 'refresh': refresh}
        