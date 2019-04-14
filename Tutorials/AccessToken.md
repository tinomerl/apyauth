# How to get an Access Token

Getting an Access Token is fairly easy with this library. The following Code Snippet should explain how it works.

```python
import oauth2py

# Define the clientId and clientSecret
clientid = 'xxxxx'
clientsecret = 'zzzzz'

# Initialize a Session with the Credentials and a Service name
instance = oauth2py.oauth('serviceName', clientid, clientsecret)

# Define optional Scopes and overhand the needed Endpoints
scope = ['scope1', 'scope2']
instance.oauthEndpoints(auth = 'https://example/authendpoint', token = 'https://example/tokenendpoint', refresh = 'https://example/refreshendpoint')

# Start the token Function, choose the Method and overhand the Scopes
tkn = instance.accessToken(method = 'post',scope = scope)
```
A prompt will ask you if you want to save the token between Sessions. This comes in handy if you want to refresh your Token later.
The access and refresh Token will be saved in the current working directory with the name of the service in the file extension. 
So if you define your service name as "MyService" the filename will be ".MyService-token". 
In this Manner you can easily refresh your access Token if you use the same service name when refreshing.