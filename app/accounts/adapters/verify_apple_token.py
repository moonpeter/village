import jwt
import requests
import json
from jwt.algorithms import RSAAlgorithm
from rest_framework import exceptions
from config.settings import get_secret

APPLE_PUBLIC_KEY_URL = "https://appleid.apple.com/auth/keys"


def _fetch_apple_public_key(unverified_header):
    key_payload = requests.get(APPLE_PUBLIC_KEY_URL).json()
    keys = key_payload["keys"]

    for key in keys:
        if key["kid"] == unverified_header["kid"]:
            return RSAAlgorithm.from_jwk(json.dumps(key))


def _decode_apple_user_token(apple_user_token):
    unverified_header = jwt.get_unverified_header(apple_user_token)
    public_key = _fetch_apple_public_key(unverified_header)
    try:
        token = jwt.decode(
            apple_user_token,
            public_key,
            audience=get_secret("APPLE_SOCIAL_CLIENT_ID"),
            algorithms="RS256",
        )
        return token
    except Exception:
        raise exceptions.AuthenticationFailed
