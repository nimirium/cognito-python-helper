# cognito-python-helper

Helper methods for AWS Cognito User Pool.

In this repository I will explain the expected flow of a program that uses cognito, and will present two main helper 
methods - one to get or refresh cognito tokens, the other is to verify the id_token.

Before you start, you should create a Cognito User Pool, add an App Client to it, and configure a cognito domain. 
All of this can be done in the AWS Cognito console.

*The flow assumes you are using Cognito Hosted UI, but this code can be useful for other cases too*

### Cognito config

First you should set the config in ``config.py``.

    cognito_config = {
        # The region where your cognito is located
        'region': 'us-west-2',
    
        # Cognito (AWS console) > User pool > App integration > Domain name
        'domain': 'COGNITO_DOMAIN',
    
        # Cognito (AWS console) > User pool > General settings > App clients
        'client_id': 'CLIENT_ID',
        'client_secret': 'CLIENT_SECRET',
    
        # Cognito (AWS console) > User pool > General settings > Pool Id
        'user_pool_id': 'USER_POOL_ID',
    
        # The URL you want to redirect to after authentication
        'redirect_uri': 'https://YOUR_WEBSITE/login/',
    }

## Flow:

1) User lands in your website for the first time. They are not authenticated. Redirect them to ``cognito_login_url`` - 
this is the **Cognito Hosted UI**.
2) In the hosted UI, they successfully log in.
3) User is redirected to ``redirect_uri``, with request parameter ``code=11111111-2222-3333-4444-555555555555``
4) We get the cognito id_token, access_token & secret_token, by ``get_cognito_tokens(code=code)``.

    ** The ID Token contains claims about the identity of the authenticated user such as name, email, and phone_number.
    
    ** The Access Token contains scopes and groups and is used to grant access to authorized resources.
    
    ** The Refresh Token contains the information necessary to obtain a new ID or access token.
    
    ** more info here: https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html

5) Store these tokens for the user
6) After an hour, id_token and access_token are expired. Backed code can automatically refresh it by using 
   ``get_cognito_tokens(refresh_token=refresh_token)``
7) After 30 days, refresh token expires. The user should be redirected to the hosted UI and will have to log in again.

##

### When the user is not logged in, redirect them to ``cognito_login_url``

    from config import cognito_login_url
    
    # (Assuming you're using flask:)
    return redirect(cognito_login_url, code=302)

### Get and verify token by authorization code

    from token_helper import get_cognito_tokens
    from jwt_helper import decode_verify_jwt

    code = '11111111-2222-3333-4444-555555555555'
    id_token, access_token, refresh_token = get_cognito_tokens(code=code)
    decoded_id_token = decode_verify_jwt(id_token)
    
### The ``decoded_id_token`` contains info about this user like email, name etc.

    user_email = decoded_id_token['email']

### Get and verify token by refresh token

    id_token, access_token, refresh_token = get_cognito_tokens(refresh_token=refresh_token)
    decoded_id_token = decode_verify_jwt(id_token)
