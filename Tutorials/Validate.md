# How to validate an Access Token
The validation of an Access Token can only be done when it is locally stored. To validate the local Access Token you can use the following code example.
```python
import oauth2py

clientid = 'xxxxx'
clientsecret = 'zzzzz'
instance = oauth2py.oauth('serviceName', clientid, clientsecret)

tkn, tknState = instance.validate()
```
The `validate` method returns a tuple. The first value will be the Access Token or the Refresh Token. Depending on the current Expiry Date of the Access Token. The second value will be a boolean with the result of the validation.

## Exceptions
### No Refresh Token
Depending on the presence of a local saved Refresh Token you may get the Refresh Token or a string saying `NoRefreshTokenFound` as the tuples first value. The latter is the case if there is no locally saved Refresh Token present.

### No Expiry Date
Some Token Endpoint don't return a value when the Access Token will expire. If this is the case the validate Function will print `No token or expiry Date found for serviceName in the current environment.` to the console and return a tuple with the following values `'NoAccessTokenFound', False`.