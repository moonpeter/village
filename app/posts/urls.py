from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostListCreateAPIView.as_view()),
    path("<int:pk>/", views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path("poll/<int:pk>/", views.PollDeleteAPIView.as_view()),
    path("<int:pk>/comments/", views.CommentCreateAPIView.as_view()),
    path("comments/<int:pk>/", views.CommentRetrieveUpdateDestroyAPIView.as_view()),
    path("<int:pk>/comments/list/", views.CommentListAPIView.as_view()),
    path("comments/<int:pk>/reply/", views.ReplyCreateAPIView.as_view()),
    path("comments/reply/<int:pk>/", views.ReplyRetrieveUpdateDestroyAPIView.as_view()),
    path("<int:pk>/like/", views.PostLikeAPIView.as_view()),
    path("<int:pk>/save/", views.PostSaveAPIView.as_view()),
    path("<int:pk>/block/", views.PostBlockAPIView.as_view()),
    path("comments/<int:pk>/like/", views.CommentLikeAPIView.as_view()),
    path("reply/<int:pk>/like/", views.ReplyLikeAPIView.as_view()),
    path("search/", views.SearchListAPIView.as_view()),
    path("reply/<int:pk>/", views.ReplyDetailAPIView.as_view()),
    path("comments/<int:pk>/reply/list/", views.CommentDetailAPIView.as_view()),
]
