from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from dj_rest_auth.registration.views import LoginView
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.serializers import JWTSerializer

from django.contrib.auth import get_user_model
from django.db.models import Q

from posts.models import Post, PostComment

from .adapters.kakaoadapter import SignupKakaoOAuth2Adapter, SigninKakaoOAuth2Adapter
from .adapters.googleadapter import SignupGoogleOAuth2Adapter, SigninGoogleOAuth2Adapter
from .adapters.appleadapter import SignupAppleOAuth2Adapter, SigninAppleOAuth2Adapter
from .adapters.naveradapter import SignupNaverOAuth2Adapter, SigninNaverOAuth2Adapter

from .serializers import (
    CustomSocialSignupSigninSerializer,
    CustomSocialLoginSerializer,
    UserSerializer,
    UserSelectedPostListSerializer,
    UserInformationSerializer,
)


class CustomLoginView(LoginView):
    def login(self):
        self.user = self.serializer.validated_data["user"]
        self.access_token, self.refresh_token = jwt_encode(self.user)

    def post(self, request, *args, **kwargs):
        provider_name = request.data.get("provider", None)
        if provider_name not in self.provider:
            return Response(
                {"provider": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            self.adapter_class = self.provider[provider_name]
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        data = {
            "user": self.user,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
        }
        serializer = JWTSerializer(
            instance=data,
            context=self.get_serializer_context(),
        )
        return Response(
            {
                "Authorization": f"Bearer {serializer.data['access_token']}",
                "Refresh-Token": serializer.data["refresh_token"],
            },
            status=status.HTTP_200_OK,
        )


######## 회원가입, 로그인 API
class CustomSignupAPI(CustomLoginView):
    serializer_class = CustomSocialSignupSigninSerializer
    provider = {
        "kakao": SignupKakaoOAuth2Adapter,
        "google": SignupGoogleOAuth2Adapter,
        "apple": SignupAppleOAuth2Adapter,
        "naver": SignupNaverOAuth2Adapter,
    }


####### 로그인 API
class CustomSigninAPI(CustomLoginView):
    serializer_class = CustomSocialLoginSerializer
    provider = {
        "kakao": SigninKakaoOAuth2Adapter,
        "google": SigninGoogleOAuth2Adapter,
        "apple": SigninAppleOAuth2Adapter,
        "naver": SigninNaverOAuth2Adapter,
    }


class NicknameDuplicationCheckingAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        nickname = request.GET.get("nickname")

        if not nickname:
            return Response(
                {
                    "code": "VAE0005",
                    "error": "empty nickname parameter",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = get_user_model().objects.get(nickname=nickname)
            if user:
                return Response(
                    {
                        "code": "VAE0006",
                        "duplicate": True,
                    },
                    status=status.HTTP_412_PRECONDITION_FAILED,
                )
        except get_user_model().DoesNotExist:
            return Response(
                {
                    "duplicate": False,
                },
                status=status.HTTP_200_OK,
            )


class UserDetailDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serialzer = UserSerializer(request.user, context=request)
        return Response(serialzer.data)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(data={"User was deleted"}, status=status.HTTP_204_NO_CONTENT)


class UserPostListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInformationSerializer

    def get_queryset(self):
        queryset = get_user_model().objects.filter(pk=self.request.user.pk)
        return queryset


class UserLikeListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSelectedPostListSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        queryset = queryset.filter(postlike__user=self.request.user)
        return queryset


class UserSavedListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSelectedPostListSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        queryset = queryset.filter(saved_post_set__nickname=self.request.user)
        return queryset


class UserInformationView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UserSelectedPostListSerializer
    queryset = get_user_model().objects.all()


class UserBlockedListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSelectedPostListSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        queryset = queryset.filter(blockedpost__user=self.request.user)
        return queryset
