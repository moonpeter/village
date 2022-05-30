from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from . import views

urlpatterns = [
    path("social/signin/", views.CustomSigninAPI.as_view()),
    path("social/signup/", views.CustomSignupAPI.as_view()),
    path("nickname/", views.NicknameDuplicationCheckingAPI.as_view()),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/me/", views.UserDetailDeleteAPIView.as_view()),
    path("users/me/posts/", views.UserPostListAPIView.as_view()),
    path("users/me/like/", views.UserLikeListAPIView.as_view()),
    path("users/me/save/", views.UserSavedListAPIView.as_view()),
    path("users/me/block/", views.UserBlockedListAPIView.as_view()),
    path("users/<int:pk>/", views.UserInformationView.as_view()),
]
