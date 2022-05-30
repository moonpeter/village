from django.contrib.auth import get_user_model
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from rest_framework import exceptions
from accounts.adapters.appleprovider import CustomAppleProvider
from accounts.adapters.verify_apple_token import _decode_apple_user_token
from accounts.exceptions import BAD_REQUEST, PreconditionFailed


class SignupAppleOAuth2Adapter(OAuth2Adapter):
    provider_id = CustomAppleProvider.id

    def complete_login(self, request, app, token, **kwargs):
        try:
            decode = _decode_apple_user_token(token.token)
            extra_data = decode
            if extra_data["iss"] != "https://appleid.apple.com":
                raise exceptions.AuthenticationFailed
        except Exception:
            raise exceptions.AuthenticationFailed
        if "email" not in extra_data:
            raise PreconditionFailed("-1")
        try:
            user = get_user_model().objects.get(email=extra_data["email"])
            if user:
                raise BAD_REQUEST
            login = self.get_provider().sociallogin_from_response(request, extra_data)
            return (login, user)

        except get_user_model().DoesNotExist:
            login = self.get_provider().sociallogin_from_response(request, extra_data)
            return (login, None)


class SigninAppleOAuth2Adapter(OAuth2Adapter):
    provider_id = CustomAppleProvider.id

    def complete_login(self, request, app, token, **kwargs):
        try:
            decode = _decode_apple_user_token(token.token)
            extra_data = decode
            if extra_data["iss"] != "https://appleid.apple.com":
                raise exceptions.AuthenticationFailed
        except Exception:
            raise exceptions.AuthenticationFailed
        if "email" not in extra_data:
            raise PreconditionFailed("-1")

        login = self.get_provider().sociallogin_from_response(request, extra_data)
        try:
            user = get_user_model().objects.get(email=extra_data["email"])
        except get_user_model().DoesNotExist:
            raise PreconditionFailed(0)
        return (login, user)
