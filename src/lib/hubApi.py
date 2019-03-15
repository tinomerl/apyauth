
#.....Oauth 2.0 Wrapper.....#
#.....Send credentials......#
#.......Receive Token.......#
#.....Author Tino Merl......#
#........(c) 2019...........#
#..........v0.1.............#

# Wrapper for Api Calls with Hubspot
import requests
import json
import ast
import pandas as pd

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

    def call(self,url):
        self.headers = {'Authorization':  'Bearer ' + self.tkn, 'Content-Type' : 'application/json'}
        self.res = requests.get(url, headers = self.headers)
        self.res.content
        return ast.literal_eval(self.res.content)

    def anal_resToDf(self,res):
        print('DF')
        if self.data == 'breakdown':
            if self.breakdown == 'sources':
                self.df = pd.DataFrame()
                self.dictKeys = list(res)
                for d in self.dictKeys:
                    self.tempList = self.res[d]
                    self.subLists = len(self.tempList)
                    for i in self.subLists:
                        self.subDict = self.tempList[i]
                        self.tempDf = pd.DataFrame.from_dict(self.subDict)
                        self.tempDf['date'] = d
                        self.df = self.df.append(self.tempDf)
        return self.df

    def analytics(self, data, breakdown = 'totals', timePeriod = 'total', start = '', end = ''):
       self.endpoint = self.urls['calls']['analytics']
       self.data = data
       if data == 'breakdown':
           self.breakdown = breakdown
           self.timeperiod = timePeriod
           self.start = start
           self.end = end
           return self.analyticsBreakdown()
    
    def analyticsBreakdown(self):
        print('analytics breakdown')
        self.addUrl = "/".join([self.breakdown, self.timeperiod])
        self.params = "&".join(['start=' + self.start, 'end=' + self.end]) 
        self.urlBuild = self.urls['base'] + self.endpoint + self.addUrl + '?' + self.params
        self.res = self.call(self.urlBuild)

        return self.anal_resToDf(self.res)