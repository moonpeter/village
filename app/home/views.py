from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounts.models import SavedCompetition

from common.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlySub

from .models import (
    CompetitionComment,
    CompetitionCommentLike,
    CompetitionLike,
    CompetitionOfThisWeek,
    CompetitionReply,
    CompetitionReplyLike,
)

from .serializers import (
    CompetitionSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
    ReplyCreateSerializer,
    ReplySerializer,
    ReplyUpdateSerializer,
    CompetitionSaveSerializer,
    CompetitionLikeSerializer,
    CommentLikeSerializer,
    ReplyLikeSerializer,
)


class CompetitionOfThisWeekDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = CompetitionOfThisWeek.objects.first()
        context = {"request": request}
        serializer = CompetitionSerializer(queryset, context=context)
        return Response(serializer.data)


class CompetitionDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompetitionSerializer
    queryset = CompetitionOfThisWeek.objects.all()


class CompetitionListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompetitionSerializer
    queryset = CompetitionOfThisWeek.objects.all()


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = CompetitionComment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            competition=CompetitionOfThisWeek.objects.get(
                pk=self.request.parser_context["kwargs"]["pk"]
            ),
            image=self.request.data.get("images"),
        )


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompetitionComment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer
        if self.request.method == "PUT":
            return CommentUpdateSerializer


class CommentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]

        queryset = CompetitionComment.objects.filter(competition__pk=pk)
        return queryset


class ReplyCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CompetitionReply.objects.all()
    serializer_class = ReplyCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            competition_comment=CompetitionComment.objects.get(
                pk=self.request.parser_context["kwargs"]["pk"]
            ),
            image=self.request.data.get("imgaes"),
        )


class ReplyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompetitionReply.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReplySerializer
        if self.request.method == "PUT":
            return ReplyUpdateSerializer


class CompetitionLikeAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompetitionLikeSerializer
    queryset = CompetitionLike.objects.all()

    def perform_create(self, serializer):
        competition = CompetitionOfThisWeek.objects.get(
            pk=self.request.parser_context["kwargs"]["pk"]
        )
        user = self.request.user
        competition_like = CompetitionLike.objects.filter(
            competition=competition, user=user
        )
        if competition_like.exists():
            competition_like.delete()
        else:
            serializer.save(user=user, competition=competition)


class CompetitionSaveAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompetitionSaveSerializer
    queryset = SavedCompetition.objects.all()

    def perform_create(self, serializer):
        competition = CompetitionOfThisWeek.objects.get(
            pk=self.request.parser_context["kwargs"]["pk"]
        )
        user = self.request.user
        saved_competition = SavedCompetition.objects.filter(
            competition=competition, user=user
        )
        if saved_competition.exists():
            saved_competition.delete()
        else:
            serializer.save(user=user, competition=competition)


class CommentLikeAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentLikeSerializer
    queryset = CompetitionCommentLike.objects.all()

    def perform_create(self, serializer):
        comment = CompetitionComment.objects.get(
            pk=self.request.parser_context["kwargs"]["pk"]
        )
        user = self.request.user
        comment_like = CompetitionCommentLike.objects.filter(
            competition_comment=comment, user=user
        )
        if comment_like.exists():
            comment_like.delete()
        else:
            serializer.save(user=user, competition_comment=comment)


class ReplyLikeAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReplyLikeSerializer
    queryset = CompetitionReplyLike.objects.all()

    def perform_create(self, serializer):
        reply = CompetitionReply.objects.get(
            pk=self.request.parser_context["kwargs"]["pk"]
        )
        user = self.request.user
        reply_like = CompetitionReplyLike.objects.filter(
            competition_reply=reply, user=user
        )
        if reply_like.exists():
            reply_like.delete()
        else:
            serializer.save(competition_reply=reply, user=user)


class ReplyDetailAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReplySerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        queryset = CompetitionReply.objects.filter(pk=pk)
        return queryset
