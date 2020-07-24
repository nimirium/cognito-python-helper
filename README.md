# cognito-python-helper

Helper methods for AWS Cognito.

Flow:
1) User lands in our website for the first time. They have no valid id_token. Redirect to ``cognito_login_url`` 
   - Cognito Hosted UI.
2) In the hosted UI, they successfully log in.
3) User is redirected to ``redirect_uri``, with request parameter ``code=11111111-2222-3333-4444-555555555555``
4) We get the cognito id_token, access_token & secret_token, by ``get_cognito_tokens(code=code)``.

.. note::
    ** The ID Token contains claims about the identity of the authenticated user such as name, email, and phone_number.
    ** The Access Token contains scopes and groups and is used to grant access to authorized resources.
    ** The Refresh Token contains the information necessary to obtain a new ID or access token.
    ** more info here: https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html

5) Store these tokens for the user
6) After an hour, id_token expires. Backed code should automatically refresh it by using 
   ``get_cognito_tokens(refresh_token=refresh_token)``
7) After 30 days, refresh token expires. The user should be redirected to the hosted UI and will have to log in again.

# When the user is not logged in, redirect them to ``cognito_login_url``

.. code-block:: python

    from config import cognito_login_url

# Get and verify token by authorization code

.. code-block:: python

    from token_helper import get_cognito_tokens
    from jwt_helper import decode_verify_jwt

    code = '11111111-2222-3333-4444-555555555555'
    id_token, access_token, refresh_token = get_cognito_tokens(code=code)
    decoded_id_token = decode_verify_jwt(id_token)
    
# decoded_id_token contains info about this user like email, name etc.

.. code-block:: python

    user_email = decoded_id_token['email']

# Get and verify token by refresh token

.. code-block:: python

    id_token, access_token, refresh_token = get_cognito_tokens(refresh_token=refresh_token)
    decoded_id_token = decode_verify_jwt(id_token)
