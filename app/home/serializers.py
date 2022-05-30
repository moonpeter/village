from rest_framework import serializers
from accounts.models import SavedCompetition

from accounts.serializers import UserSerializer

from .models import (
    CompetitionComment,
    CompetitionCommentLike,
    CompetitionLike,
    CompetitionOfThisWeek,
    CompetitionChoice,
    CompetitionReply,
    CompetitionReplyLike,
)


class CompetitionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionChoice
        fields = ("choice_text", "votes")


class CompetitionSerializer(serializers.ModelSerializer):
    choice = CompetitionChoiceSerializer(many=True)
    number_of_comments_and_reply = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    number_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = CompetitionOfThisWeek
        fields = (
            "pk",
            "created",
            "modified",
            "closing_date",
            "title",
            "content",
            "hits",
            "number_of_comments_and_reply",
            "is_saved",
            "is_liked",
            "number_of_likes",
            "choice",
        )

    def get_number_of_comments_and_reply(self, instance):
        number_of_comments = instance.competitioncomment_set.count()
        comment_all = instance.competitioncomment_set.all()
        number_of_reply = 0
        for comment in comment_all:
            number_of_reply += comment.reply.count()
        return number_of_comments + number_of_reply

    def get_is_saved(self, instance):
        saved_post = instance.saved_competition_set.filter(
            nickname=self.context.get("request").user
        )
        if saved_post:
            return True
        else:
            return False

    def get_is_liked(self, instance):
        competition_like = instance.competitionlike_set.filter(
            user=self.context.get("request").user.pk
        )
        if competition_like:
            return True
        else:
            return False

    def get_number_of_likes(self, instance):
        number_of_likes = instance.competitionlike_set.count()
        return number_of_likes


class CommentCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = CompetitionComment
        fields = ("content", "image")


class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer()
    number_of_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = CompetitionReply
        fields = (
            "pk",
            "created",
            "modified",
            "author",
            "content",
            "image",
            "is_liked",
            "number_of_likes",
        )

    def get_number_of_likes(self, instance):
        number_of_likes = instance.competitionreplylike_set.count()
        return number_of_likes

    def get_is_liked(self, instance):
        reply_like = instance.competitionreplylike_set.filter(
            user=self.context.get("request").user.pk
        )
        if reply_like:
            return True
        else:
            return False


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    is_liked = serializers.SerializerMethodField()
    number_of_likes = serializers.SerializerMethodField()
    reply = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = CompetitionComment
        fields = (
            "pk",
            "created",
            "modified",
            "author",
            "content",
            "image",
            "is_liked",
            "number_of_likes",
            "reply",
        )

    def get_number_of_likes(self, instance):
        number_of_likes = instance.competitioncommentlike_set.count()
        return number_of_likes

    def get_is_liked(self, instance):
        comment_like = instance.competitioncommentlike_set.filter(
            user=self.context.get("request").user.pk
        )
        if comment_like:
            return True
        else:
            return False


class CommentUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = CompetitionComment
        fields = ("content", "image")

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        try:
            images_data = self.context.get("request").data.pop("images")
        except:
            images_data = None
            instance.image = None
        if images_data is not None:
            instance.image = images_data[0]

        instance.save()
        return instance

    def to_representation(self, instance):
        return CommentSerializer(instance, context=self.context).data


class ReplyCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = CompetitionReply
        fields = ("content", "image")


class ReplyUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = CompetitionReply
        fields = ("content", "image")

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        try:
            images_data = self.context.get("request").data.pop("images")
        except:
            images_data = None
            instance.image = None
        if images_data is not None:
            instance.image = images_data[0]

        instance.save()
        return instance

    def to_representation(self, instance):
        return ReplySerializer(instance, context=self.context).data


class CompetitionLikeSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = CompetitionLike
        fields = ("likes",)

    def get_likes(self, instance):
        competition_pk = self.context.get("request").parser_context.get("kwargs")["pk"]
        competition_instance = CompetitionOfThisWeek.objects.get(pk=competition_pk)
        number_of_likes = competition_instance.competitionlike_set.count()
        if competition_instance.competitionlike_set.all().filter(
            user=self.context.get("request").user
        ):
            is_liked = True
        else:
            is_liked = False
        likes = {
            "number_of_likes": number_of_likes,
            "is_liked": is_liked,
        }

        return likes


class CompetitionSaveSerializer(serializers.ModelSerializer):
    saved = serializers.SerializerMethodField()

    class Meta:
        model = SavedCompetition
        fields = ("saved",)

    def get_saved(self, instance):
        competition_pk = self.context.get("request").parser_context.get("kwargs")["pk"]
        competition_instance = CompetitionOfThisWeek.objects.get(pk=competition_pk)
        if competition_instance.saved_competition_set.all().filter(
            nickname=self.context.get("request").user
        ):
            is_saved = True
        else:
            is_saved = False
        return is_saved


class CommentLikeSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = CompetitionCommentLike
        fields = ("likes",)

    def get_likes(self, instance):
        comment_pk = self.context.get("request").parser_context.get("kwargs")["pk"]
        comment_instance = CompetitionComment.objects.get(pk=comment_pk)
        number_of_likes = comment_instance.competitioncommentlike_set.count()
        if comment_instance.competitioncommentlike_set.all().filter(
            user=self.context.get("request").user
        ):
            is_liked = True
        else:
            is_liked = False
        likes = {
            "number_of_likes": number_of_likes,
            "is_liked": is_liked,
        }
        return likes


class ReplyLikeSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = CompetitionReplyLike
        fields = ("likes",)

    def get_likes(self, instance):
        reply_pk = self.context.get("request").parser_context.get("kwargs")["pk"]
        reply_instance = CompetitionReply.objects.get(pk=reply_pk)
        number_of_likes = reply_instance.competitionreplylike_set.count()
        if reply_instance.competitionreplylike_set.all().filter(
            user=self.context.get("request").user
        ):
            is_liked = True
        else:
            is_liked = False
        likes = {
            "number_of_likes": number_of_likes,
            "is_liked": is_liked,
        }

        return likes
