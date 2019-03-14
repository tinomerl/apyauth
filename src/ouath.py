# Hubspot API with Python
## OAUTH 2.0

from requests_oauthlib import oauth2_session
from oauthlib.oauth2 import LegacyApplicationClient
import requests_oauthlib
import os

# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

### General Creds
appId = "189488"
appName = "p7-reporting-test"
clientId = "6861bfc7-f088-4720-a689-e49030fe8e44"
clientSecret = "d603bb1e-1435-4ece-b11c-6be56ca31ad4"

### Base URLs
authUrl = "https://app.hubspot.com/oauth/authorize"
tokenUrl = "https://api.hubapi.com/oauth/v1/token"
redirectUri = "http://localhost:1410/"
oauth = oauth2_session.OAuth2Session(client = LegacyApplicationClient(client_id = clientId))

### Select a Scope
scope = ["business-intelligence", "oauth"]

### Build Auth URL
buildUrl = authUrl + "?client_id=" + clientId + "&scope=" + scope + "&redirect_uri=" + redirectUri

#oauth = requests_oauthlib.OAuth2Session(clientId,redirect_uri = redirectUri, scope=scope)
authorizationURL, state = oauth.authorization_url(authUrl)

### Exchange Security Codes
print('Please go to %s and authorize access.') % authorizationURL
authorization_response = raw_input('Enter the full callback URL')

### Get a Token
token = oauth.fetch_token(token_url = tokenUrl, client_id = clientId, client_secret = clientSecret, authorization_response = authorization_response)
