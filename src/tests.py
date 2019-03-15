import sys
sys.path.insert(0,'./src/lib')
import oauth2class
import hubApi

import ast

clientid = '6861bfc7-f088-4720-a689-e49030fe8e44'
clientsecret = 'd603bb1e-1435-4ece-b11c-6be56ca31ad4'
instanz = oauth2class.oauth2(clientid, clientsecret)
scope = ['contacts', 'content', 'automation', 'business-intelligence', 'forms']
instanz.authEndpoints('https://app.hubspot.com/oauth/authorize',' https://api.hubapi.com/oauth/v1/token')
instanz.authUrlBuild(scope)
tkn = instanz.getToken()

hub = hubApi.HubApi(tkn)
data = hub.analytics('breakdown', start = "20190101", end = "20190102", breakdown= 'sources', timePeriod= 'daily')


len(data)
import pandas as pd
import json

data.keys()


data[list(data)[0]][1]

df = pd.DataFrame()


json.dumps(data['breakdowns'])

pd.read_json(json.dumps(data['breakdowns']), orient = "records")

data