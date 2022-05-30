import requests
from django.contrib.auth import get_user_model
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from rest_framework import exceptions
from accounts.exceptions import BAD_REQUEST, PreconditionFailed


class SignupNaverOAuth2Adapter(NaverOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        if resp.status_code >= 400:
            raise exceptions.AuthenticationFailed
        extra_data = resp.json().get("response")
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


class SigninNaverOAuth2Adapter(NaverOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        req = requests.get(self.profile_url, headers=headers)
        if req.status_code >= 400:
            raise exceptions.AuthenticationFailed
        extra_data = req.json().get("response")
        if "email" not in extra_data:
            raise PreconditionFailed("-1")

        login = self.get_provider().sociallogin_from_response(request, extra_data)
        try:
            user = get_user_model().objects.get(email=extra_data["email"])
        except get_user_model().DoesNotExist:
            raise PreconditionFailed(0)
        return (login, user)
