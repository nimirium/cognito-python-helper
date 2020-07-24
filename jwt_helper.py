__author__ = 'Sophie Fogel'

import logging
from typing import Tuple

import requests
from requests.auth import HTTPBasicAuth

from config import cognito_config





class CognitoAuthenticationError(Exception):
    pass


def get_cognito_tokens(code=None, refresh_token=None) -> Tuple[str, str, str]:
    """
    Get / refresh cognito tokens.

    Option 1: by code
    We receive authentication code from cognito hosted UI, after a successful log-in.
    Example redirect: https://YOUR_WEBSITE/?code=11111111-2222-3333-4444-555555555555
    This code can be used by this method to retrieve cognito id, access & refresh tokens.

    Option 2: by refresh_token
    In this scenario the user is already logged in, but his token has expired.
    Tokens expire after an hour. Refresh token expires after 30 days. Refresh token can be used to get id_token.

    :return: Tuple with id_token, access_token, refresh_token
    :raises: CognitoAuthenticationError
    """

    assert (code or refresh_token) and not (code and refresh_token), \
        f"You must provide `cognito_code` or `refresh_token` (one of them only)"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    url = f"https://{cognito_config['domain']}.auth.{cognito_config['region']}.amazoncognito.com/oauth2/token"
    data = {
        'client_id': cognito_config['client_id'],
        'redirect_uri': cognito_config['redirect_uri'],
    }
    if code:
        data['code'] = code
        data['grant_type'] = 'authorization_code'
    elif refresh_token:
        data['refresh_token'] = refresh_token
        data['grant_type'] = 'refresh_token'

    logging.debug("Getting cognito tokens - Sending POST request to %s with headers=%s data=%s"
                  % (url, str(headers), str(data)))

    response = requests.post(url, headers=headers, data=data,
                             auth=HTTPBasicAuth(cognito_config['client_id'], cognito_config['client_secret']))

    if response.status_code != 200:
        logging.error(f"Failed to get/refresh cognito tokens. data={data}.")
        raise CognitoAuthenticationError(f"Failed to get/refresh cognito tokens. data={data}.")

    tokens = response.json()

    if code:
        return tokens['id_token'], tokens['access_token'], tokens['refresh_token']
    else:
        return tokens['id_token'], tokens['access_token'], refresh_token
