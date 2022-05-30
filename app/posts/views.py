from rest_framework import generics

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from django.db.models import Q

from accounts.models import SavedPost, BlockedPost

from .models import (
    PollQuestion,
    Post,
    PostComment,
    PostCommentLike,
    PostLike,
    PostReply,
    PostReplyLike,
)
from .serializers import (
    CommentSerializer,
    PostLikeSerializer,
    PostSaveSerializer,
    PostBlockSerializer,
    CommentLikeSerializer,
    ReplyLikeSerializer,
    PostSerializer,
    PostDetailSerializer,
    PostCreatSerializer,
    PostUpdateSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
    ReplyCreateSerializer,
    ReplySerializer,
    ReplyUpdateSerializer,
)
from common.permissions import (
    IsOwnerOrReadOnly,
    IsOwnerOrReadOnlySub,
)
from django.contrib.auth import get_user_model


class PostListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    queryset = queryset.select_related("author", "pollquestion")
    queryset = queryset.prefetch_related(
        "postimage_set",
        "pollquestion__pollchoice_set",
        "postcomment_set",
        "postcomment_set__reply",
        "postlike_set",
        "postlike_set__user",
    )

    def get_queryset(self):
        condition = Q()

        category = self.request.query_params.get("category")
        if category:
            category_list = category.split(",")
            condition = Q(category__contains=[category_list[0]])
            for category in category_list[1:]:
                condition |= Q(category__contains=[category])

        mbti_tag = self.request.query_params.get("mbti-tag")
        if mbti_tag:
            condition &= Q(mbti_tags__contains=[mbti_tag])

        queryset = self.queryset.filter(condition)
        queryset = queryset.exclude(
            Q(blockedpost__isnull=False) & Q(blockedpost__user=self.request.user.id)
        )

        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostSerializer
        if self.request.method == "POST":
            return PostCreatSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostDetailSerializer
        if self.request.method == "PUT":
            return PostUpdateSerializer


class PollDeleteAPIView(generics.DestroyAPIView):
    queryset = PollQuestion.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlySub]


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = PostComment.objects.all()
    queryset = queryset.select_related(
        "author",
    )
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=Post.objects.get(pk=self.request.parser_context["kwargs"]["pk"]),
            image=self.request.data.get("images"),
        )


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostComment.objects.all()
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

        queryset = PostComment.objects.filter(post__pk=pk)
        queryset = queryset.prefetch_related(
            "reply", "postcommentlike_set", "reply__postreplylike_set"
        )
        queryset = queryset.select_related("author")
        return queryset


class CommentDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    queryset = PostComment.objects.all()


class ReplyCreateAPIView(generics.CreateAPIView):
    queryset = PostReply.objects.all()
    queryset = queryset.select_related(
        "author",
    )
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReplyCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_comment=PostComment.objects.get(
                pk=self.request.parser_context["kwargs"]["pk"]
            ),
            image=self.request.data.get("images"),
        )


class ReplyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostReply.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReplySerializer
        if self.request.method == "PUT":
            return ReplyUpdateSerializer


class ReplyDetailAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReplySerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]

        queryset = PostReply.objects.filter(pk=pk)
        return queryset


class PostLikeAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.request.parser_context["kwargs"]["pk"])
        user = self.request.user
        post_like = PostLike.objects.filter(post=post, user=user)
        if post_like.exists():
            post_like.delete()
        else:
            serializer.save(user=user, post=post)


class PostSaveAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSaveSerializer
    queryset = SavedPost.objects.all()

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.request.parser_context["kwargs"]["pk"])
        user = self.request.user
        saved_post = SavedPost.objects.filter(post=post, user=user)
        if saved_post.exists():
            saved_post.delete()
        else:
            serializer.save(user=user, post=post)


class PostBlockAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostBlockSerializer
    queryset = BlockedPost.objects.all()

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.request.parser_context["kwargs"]["pk"])
        user = self.request.user
        blocked_post = BlockedPost.objects.filter(post=post, user=user)
        if blocked_post.exists():
            blocked_post.delete()
        else:
            serializer.save(user=user, post=post)


class CommentLikeAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentLikeSerializer
    queryset = PostCommentLike.objects.all()

    def perform_create(self, serializer):
        comment = PostComment.objects.get(
            pk=self.request.parser_context["kwargs"]["pk"]
        )
        user = self.request.user
        comment_like = PostCommentLike.objects.filter(post_comment=comment, user=user)
        if comment_like.exists():
            comment_like.delete()
        else:
            serializer.save(user=user, post_comment=comment)


class ReplyLikeAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReplyLikeSerializer
    queryset = PostReplyLike.objects.all()

    def perform_create(self, serializer):
        reply = PostReply.objects.get(pk=self.request.parser_context["kwargs"]["pk"])
        user = self.request.user
        reply_like = PostReplyLike.objects.filter(post_reply=reply, user=user)
        if reply_like.exists():
            reply_like.delete()
        else:
            serializer.save(user=user, post_reply=reply)


class SearchListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    queryset = queryset.select_related("author", "pollquestion")
    queryset = queryset.prefetch_related(
        "postimage_set",
        "pollquestion__pollchoice_set",
        "postcomment_set",
        "postcomment_set__reply",
        "postlike_set",
        "postlike_set__user",
    )

    def get_queryset(self):
        search_word = self.request.query_params.get("search-word")
        queryset = self.queryset.filter(
            Q(title__contains=search_word)
            | Q(content__contains=search_word)
            | Q(pollquestion__title__contains=search_word)
            | Q(pollquestion__pollchoice__choice_text__contains=search_word)
        )
        return queryset
