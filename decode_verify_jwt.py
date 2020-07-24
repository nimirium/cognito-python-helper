# Copyright 2017-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.
#
# -
#
# Original code:
# https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py
# This code was modified here by Sophie Fogel


import logging
import time
from typing import Union, Dict, List

import requests
from jose import jwk, jwt
from jose.utils import base64url_decode

from config import cognito_config


def download_jwks() -> List[Dict]:
    """
    Download public JWK, that can be used to validate JWT.
    :return: list of cognito public keys
    """

    keys_url = f"https://cognito-idp.{cognito_config['region']}.amazonaws.com/{cognito_config['user_pool_id']}/.well-known/jwks.json"
    response = requests.get(keys_url)
    keys = response.json()['keys']
    return keys


_jwks = None  # JWKS - public keys that can be used to decode JWT.


def get_jwks():
    global _jwks
    if not _jwks:
        _jwks = download_jwks()
    return _jwks


def decode_verify_jwt(token: str) -> Union[Dict, bool]:
    """
    Returns de-coded JWT. If there is something wrong with with the token, will return False.
    """

    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    keys = get_jwks()
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        logging.info('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        logging.info('Signature verification failed')
        return False
    logging.info('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        logging.info('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != cognito_config['client_id']:
        logging.info('Token was not issued for this audience')
        return False
    # now we can use the claims
    logging.info(claims)
    return claims
