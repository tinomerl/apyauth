# Wrapper for Api Calls with Hubspot
class HubApi:
    
    def __init__(self,tkn):
        self.tkn = tkn
        self.urls = {'base': 'https://api.hubapi.com/', 
        'calls' : {
            'analytics' : 'analytics/v2/reports/',
            'emails': '',
            'forms' : '',
            'contacts' : '',
            'blog' : '',
            'templates' : ''
        }
        }

    def analytics(self):
        print(self.urls['base'] + self.urls['calls']['analytics'])

hub = HubApi(tkn)
hub.analytics()