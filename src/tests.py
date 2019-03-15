import sys
sys.path.insert(0,'./src/lib')
import oauth2class


clientid = '6861bfc7-f088-4720-a689-e49030fe8e44'
clientsecret = 'd603bb1e-1435-4ece-b11c-6be56ca31ad4'
instanz = oauth2class.oauth2(clientid, clientsecret)
scope = ['contacts', 'content', 'automation', 'business-intelligence', 'forms']
instanz.authEndpoints('https://app.hubspot.com/oauth/authorize',' https://api.hubapi.com/oauth/v1/token')
instanz.authUrlBuild(scope)
tkn = instanz.getToken()
tkn

import requests
import ast

headers = {'Authorization':  'Bearer ' + tkn, 'Content-Type' : 'application/json'}

res = requests.get('https://api.hubapi.com/analytics/v2/reports/sources/total?start=20190101&end=20190101', headers = headers)

ast.literal_eval(res.content)