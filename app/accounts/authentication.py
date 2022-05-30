from django.http import Http404
from rest_framework import HTTP_HEADER_ENCODING

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser

import jwt

from config.settings import get_secret

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

AUTH_HEADER_TYPES_BYTES = set(h.encode(HTTP_HEADER_ENCODING) for h in AUTH_HEADER_TYPES)


class CustomAuthenticationCore(JWTAuthentication):
    def get_refresh_token(self, request):
        return request.headers.get("Refresh-Token", "")

    def get_validated_token(self, raw_token, refresh_token):
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            if not raw_token or not refresh_token:
                return "Invalid"
            try:
                try:
                    token = AuthToken(raw_token)
                except Exception:
                    jwt.decode(
                        jwt=raw_token,
                        key=get_secret("SECRET_KEY"),
                        algorithms=["HS512"],
                    )
                refresh = jwt.decode(
                    jwt=refresh_token,
                    key=get_secret("SECRET_KEY"),
                    algorithms=["HS512"],
                )
                # 추후에 블랙리스트 구현 후에 검증 필요
                # if self.check_token_blacklisst(refresh["jti"]):
                #     return "Invalid"
                return token
            except (jwt.exceptions.InvalidSignatureError, jwt.DecodeError):
                return "Invalid"
            except jwt.exceptions.ExpiredSignatureError:
                try:
                    jwt.decode(
                        jwt=refresh_token,
                        key=get_secret("SECRET_KEY"),
                        algorithms=["HS512"],
                    )
                    refresh = RefreshToken(refresh_token)
                    # if self.check_token_blacklist(refresh["jti"]):
                    #     return "Invalid"
                    access = refresh.access_token
                    return access
                except (jwt.exceptions.InvalidSignatureError, jwt.DecodeError):
                    return "Invalid"
                except jwt.exceptions.ExpiredSignatureError:
                    return "Incalid"
            except Exception:
                return "Invalid"


class CustomAuthentication(CustomAuthenticationCore):
    def get_raw_token(self, header):
        parts = header.split()
        if len(parts) == 0:
            return None
        if parts[0] not in AUTH_HEADER_TYPES_BYTES:
            return None
        return parts[1]

    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            if not user_id:
                return None
        except (KeyError, TypeError):
            return AnonymousUser()
        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            return AnonymousUser()

        if not user.is_active:
            raise AuthenticationFailed("User is inactive")

        return user

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        refresh_token = self.get_refresh_token(request)
        validated_token = self.get_validated_token(raw_token, refresh_token)
        if (
            raw_token
            and self.get_user(validated_token) == AnonymousUser()
            and validated_token != "Invalid"
            and validated_token != "Expired"
        ):
            validated_token = "NotUser"
        return self.get_user(validated_token), validated_token


class CustomAuthenticationUserOnly(CustomAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        refresh_token = self.get_refresh_token(request)
        if not raw_token or not refresh_token:
            return None
        validated_token = self.get_validated_token(raw_token, refresh_token)
        return self.get_user(validated_token), validated_token

    def get_raw_token(self, header):
        parts = header.split()
        if len(parts) == 0:
            return None
        if parts[0] not in AUTH_HEADER_TYPES_BYTES:
            return None
        if len(parts) != 2:
            raise AuthenticationFailed(
                "Authorization header must contain two space=delimited values"
            )
        return parts[1]

    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            if not user_id:
                return None
        except (KeyError, TypeError):
            raise AuthenticationFailed

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise Http404

        if not user.is_active:
            raise AuthenticationFailed("User is inactive")

        return user
