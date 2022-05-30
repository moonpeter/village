from django.contrib.auth import get_user_model
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from google.oauth2 import id_token
from google.auth.transport import requests as g_requests
from rest_framework import exceptions
from accounts.exceptions import BAD_REQUEST, PreconditionFailed
from config.settings import get_secret


class SignupGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        try:
            extra_data = id_token.verify_oauth2_token(
                token.token,
                g_requests.Request(),
                audience=get_secret("GOOGLE_SOCIAL_CLIENT_ID"),
            )
        except Exception:
            raise exceptions.AuthenticationFailed
        if "email" not in extra_data:
            raise PreconditionFailed("-1")
        extra_data["id"] = extra_data["sub"]
        try:
            user = get_user_model().objects.get(email=extra_data["email"])
            if user:
                raise BAD_REQUEST
            login = self.get_provider().sociallogin_from_response(request, extra_data)
            return (login, user)

        except get_user_model().DoesNotExist:
            login = self.get_provider().sociallogin_from_response(request, extra_data)
            return (login, None)


class SigninGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        try:
            extra_data = id_token.verify_oauth2_token(
                token.token,
                g_requests.Request(),
                audience=get_secret("GOOGLE_SOCIAL_CLIENT_ID"),
            )
            extra_data["id"] = extra_data["sub"]
        except Exception:
            raise exceptions.AuthenticationFailed
        if "email" not in extra_data:
            raise PreconditionFailed("-1")
        extra_data["id"] = extra_data["sub"]

        login = self.get_provider().sociallogin_from_response(request, extra_data)
        try:
            user = get_user_model().objects.get(email=extra_data["email"])
        except get_user_model().DoesNotExist:
            raise PreconditionFailed(0)
        return (login, user)
