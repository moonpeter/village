import requests
from django.contrib.auth import get_user_model
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from rest_framework import exceptions
from accounts.exceptions import BAD_REQUEST, PreconditionFailed


class SignupKakaoOAuth2Adapter(KakaoOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        if resp.status_code >= 400:
            raise exceptions.AuthenticationFailed
        extra_data = resp.json()
        if "email" not in extra_data["kakao_account"]:
            raise PreconditionFailed("-1")
        try:
            user = get_user_model().objects.get(
                email=extra_data["kakao_account"]["email"]
            )
            if user:
                raise BAD_REQUEST
            login = self.get_provider().sociallogin_from_response(request, extra_data)
            return (login, user)

        except get_user_model().DoesNotExist:
            login = self.get_provider().sociallogin_from_response(request, extra_data)
            return (login, None)


class SigninKakaoOAuth2Adapter(KakaoOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        req = requests.get(self.profile_url, headers=headers)
        if req.status_code >= 400:
            raise exceptions.AuthenticationFailed
        extra_data = req.json()
        if "email" not in extra_data["kakao_account"]:
            raise PreconditionFailed("-1")

        login = self.get_provider().sociallogin_from_response(request, extra_data)
        try:
            user = get_user_model().objects.get(
                email=extra_data["kakao_account"]["email"]
            )
        except get_user_model().DoesNotExist:
            raise PreconditionFailed(0)
        return (login, user)
