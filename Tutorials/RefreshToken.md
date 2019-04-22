# How to refresh Access Token

For refreshing an Access Token there are three different scenarios. The Code Examples will provide the usage.

1. Instance where the Access Token was obtained is still running and the Access Token expired.

```python
# Same as the Access Token
import oauth2py

clientid = 'xxxxx'
clientsecret = 'zzzzz'
instance = oauth2py.oauth('serviceName', clientid, clientsecret)
scope = ['scope1', 'scope2']
instance.oauthEndpoints(auth = 'https://example/authendpoint', token = 'https://example/tokenendpoint', refresh = 'https://example/refreshendpoint')
tkn = instance.accessToken(method = 'post',scope = scope)

newTkn = instance.refreshToken()
```

2. The Instance where the Access Token was obtained is not running anymore but the Access and Refresh Token were saved in a file in the current working directory.
```python
import oauth2py

clientid = 'xxxxx'
clientsecret = 'zzzzz'
instance = oauth2py.oauth('serviceName', clientid, clientsecret)
instance.oauthEndpoints(auth = 'https://example/authendpoint', token = 'https://example/tokenendpoint', refresh = 'https://example/refreshendpoint')

newTkn = instance.refreshToken()
```

3. You have an Refresh Token saved in the clipboard.
```python
import oauth2py

clientid = 'xxxxx'
clientsecret = 'zzzzz'
instance = oauth2py.oauth('serviceName', clientid, clientsecret)
instance.oauthEndpoints(auth = 'https://example/authendpoint', token = 'https://example/tokenendpoint', refresh = 'https://example/refreshendpoint')

newTkn = instance.refreshToken()
```
Scenario 2 and 3 are mosstly the same. The difference is, that you will be prompted in the terminal to paste the refresh Token.