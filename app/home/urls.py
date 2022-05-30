from django.urls import path

from . import views

urlpatterns = [
    path("", views.CompetitionOfThisWeekDetailAPIView.as_view()),
    path("<int:pk>/", views.CompetitionDetailAPIView.as_view()),
    path("list/", views.CompetitionListAPIView.as_view()),
    path("<int:pk>/comments/", views.CommentCreateAPIView.as_view()),
    path("comments/<int:pk>/", views.CommentRetrieveUpdateDestroyAPIView.as_view()),
    path("<int:pk>/comments/list/", views.CommentListAPIView.as_view()),
    path("comments/<int:pk>/reply/", views.ReplyCreateAPIView.as_view()),
    path("comments/reply/<int:pk>/", views.ReplyRetrieveUpdateDestroyAPIView.as_view()),
    path("reply/<int:pk>/", views.ReplyDetailAPIView.as_view()),
    path("<int:pk>/like/", views.CompetitionLikeAPIView.as_view()),
    path("comments/<int:pk>/like/", views.CommentLikeAPIView.as_view()),
    path("reply/<int:pk>/like/", views.ReplyLikeAPIView.as_view()),
]
