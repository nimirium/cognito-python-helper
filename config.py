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
    'redirect_uri': 'https://YOUR_DOMAIN/login/',
}


def _validate_cognito_config():
    required_config = ['domain', 'region', 'client_id', 'client_secret', 'user_pool_id', 'redirect_uri']
    for k in required_config:
        assert k in cognito_config, f"cognito_config is missing {k}"


_validate_cognito_config()


# This is the cognito hosted UI url. When a user is not authenticated, redirect there.
# Upon a successful login, it redirects back to us with an authorization "code" request parameter.
cognito_login_url = f"https://{cognito_config['domain']}.auth.us-west-2.amazoncognito.com/login" \
                    f"?client_id={cognito_config['client_id']}" \
                    f"&response_type=code" \
                    f"&scope=aws.cognito.signin.user.admin+email+openid+phone+profile" \
                    f"&redirect_uri={cognito_config['redirect_uri']}"
