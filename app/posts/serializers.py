from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import BlockedPost, SavedPost
from .models import (
    Post,
    PostCommentLike,
    PostImage,
    PollQuestion,
    PollChoice,
    PostComment,
    PostLike,
    PostReply,
    PostReplyLike,
)
from accounts.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    image_url = serializers.SerializerMethodField()
    poll = serializers.SerializerMethodField()
    number_of_comments_and_reply = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()
    number_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "pk",
            "category",
            "mbti_tags",
            "author",
            "title",
            "content",
            "created",
            "modified",
            "image_url",
            "poll",
            "hits",
            "number_of_comments_and_reply",
            "is_liked",
            "is_blocked",
            "number_of_likes",
            # 조회수
        )

    def get_image_url(self, instance):
        imageset_list = instance.postimage_set.all()
        image_url_list = []
        # 중복 쿼리가 발생하는 부분이라 해결해야 함
        for image in imageset_list:
            post_image = PostImage.objects.get(pk=image.pk)
            image_url_list.append(post_image.image.url)
        return image_url_list

    def get_poll(self, instance):
        try:
            pollquestion = instance.pollquestion
        except AttributeError:
            poll = {}
            return poll
        poll_choice_set = pollquestion.pollchoice_set.all()
        choices_list = []
        if len(poll_choice_set) > 0:
            for choice in poll_choice_set:
                choices_list.append(
                    {
                        "pk": choice.pk,
                        "choice_text": choice.choice_text,
                        "votes": choice.votes,
                    }
                )

        poll = {
            "pk": pollquestion.pk,
            "title": pollquestion.title,
            "choice": choices_list,
        }
        return poll

    def get_number_of_comments_and_reply(self, instance):
        number_of_comments = instance.postcomment_set.count()
        comment_all = instance.postcomment_set.all()
        number_of_reply = 0
        for comment in comment_all:
            number_of_reply += comment.reply.count()
        return number_of_comments + number_of_reply

    def get_is_liked(self, instance):
        post_like = instance.postlike_set.filter(
            user=self.context.get("request").user.pk
        )
        if post_like:
            return True
        else:
            return False

    def get_is_blocked(self, instance):
        blocked_post = instance.blockedpost_set.filter(
            user=self.context.get("request").user.pk
        )
        if blocked_post:
            return True
        else:
            return False

    def get_number_of_likes(self, instance):
        number_of_likes = instance.postlike_set.count()
        return number_of_likes


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    poll = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()
    number_of_likes = serializers.SerializerMethodField()
    number_of_comments_and_reply = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "pk",
            "category",
            "mbti_tags",
            "author",
            "title",
            "content",
            "created",
            "modified",
            "image_url",
            "poll",
            "hits",
            "is_saved",
            "is_liked",
            "is_blocked",
            "number_of_comments_and_reply",
            "number_of_likes",
        )

    def get_image_url(self, instance):
        imageset_list = instance.postimage_set.all()
        image_url_list = []
        # 중복 쿼리가 발생하는 부분이라 해결해야 함
        for image in imageset_list:
            post_image = PostImage.objects.get(pk=image.pk)
            image_url_list.append(post_image.image.url)
        return image_url_list

    def get_poll(self, instance):
        try:
            pollquestion = instance.pollquestion
        except AttributeError:
            poll = {}
            return poll
        poll_choice_set = pollquestion.pollchoice_set.all()
        choices_list = []
        if len(poll_choice_set) > 0:
            for choice in poll_choice_set:
                choices_list.append(
                    {
                        "pk": choice.pk,
                        "choice_text": choice.choice_text,
                        "votes": choice.votes,
                    }
                )

        poll = {
            "pk": pollquestion.pk,
            "title": pollquestion.title,
            "choice": choices_list,
        }
        return poll

    def get_number_of_comments_and_reply(self, instance):
        number_of_comments = instance.postcomment_set.count()
        comment_all = instance.postcomment_set.all()
        number_of_reply = 0
        for comment in comment_all:
            number_of_reply += comment.reply.count()
        return number_of_comments + number_of_reply

    def get_is_saved(self, instance):
        saved_post = instance.saved_post_set.filter(
            nickname=self.context.get("request").user
        )
        if saved_post:
            return True
        else:
            return False

    def get_is_liked(self, instance):
        post_like = instance.postlike_set.filter(
            user=self.context.get("request").user.pk
        )
        if post_like:
            return True
        else:
            return False

    def get_is_blocked(self, instance):
        blocked_post = instance.blockedpost_set.filter(
            user=self.context.get("request").user.pk
        )
        if blocked_post:
            return True
        else:
            return False

    def get_number_of_likes(self, instance):
        number_of_likes = instance.postlike_set.count()
        return number_of_likes


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollQuestion
        fields = ("pk", "title")


class PostCreatedDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    poll = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "pk",
            "category",
            "mbti_tags",
            "author",
            "title",
            "content",
            "created",
            "modified",
            "image_url",
            "poll",
            "hits",
        )

    def get_image_url(self, instance):
        imageset_list = instance.postimage_set.all()
        image_url_list = []
        # 중복 쿼리가 발생하는 부분이라 해결해야 함
        for image in imageset_list:
            post_image = PostImage.objects.get(pk=image.pk)
            image_url_list.append(post_image.image.url)
        return image_url_list

    def get_poll(self, instance):
        try:
            pollquestion = instance.pollquestion
        except AttributeError:
            poll = {}
            return poll
        poll_choice_set = pollquestion.pollchoice_set.all()
        choices_list = []
        if len(poll_choice_set) > 0:
            for choice in poll_choice_set:
                choices_list.append(
                    {
                        "pk": choice.pk,
                        "choice_text": choice.choice_text,
                    }
                )

        poll = {
            "pk": pollquestion.pk,
            "title": pollquestion.title,
            "choice": choices_list,
        }
        return poll


class PostCreatSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        required=False,
        child=serializers.ImageField(use_url=True, allow_empty_file=True),
    )
    poll_question = serializers.CharField(required=False)
    poll_choices = serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = (
            "category",
            "mbti_tags",
            "title",
            "content",
            "images",
            "poll_question",
            "poll_choices",
            # "poll",
        )

    def create(self, validated_data):
        images = validated_data.pop("images", "")
        poll_question = validated_data.pop("poll_question", "")
        if poll_question:
            try:
                poll_choices = validated_data.pop("poll_choices")
            except KeyError:
                raise ValidationError
            poll_choices_list = poll_choices.split(",")

        post = super().create(validated_data)

        for image in images:
            serializer = PostImageCreateSerializer(data={"image": image})
            if serializer.is_valid():
                serializer.save(post=post)

        # Poll - question
        if poll_question:
            serializer = PollQuestionCreateSerializer(data={"title": poll_question})
            if serializer.is_valid():
                serializer.save(post=post)
                poll_question_instance = serializer.instance
            # Poll - choices
            for choice in poll_choices_list:
                serializer = PollChoiceCreateSerializer(data={"choice_text": choice})
                if serializer.is_valid():
                    serializer.save(question=poll_question_instance)
        return post

    def to_representation(self, instance):
        return PostCreatedDetailSerializer(instance, context=self.context).data


class PostImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("image",)


class PollQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollQuestion
        fields = ("title",)


class PollChoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollChoice
        fields = ("choice_text",)


class PostUpdateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        required=False,
        child=serializers.ImageField(use_url=True, allow_empty_file=True),
    )

    class Meta:
        model = Post
        fields = (
            "category",
            "mbti_tags",
            "title",
            "content",
            "images",
        )

    def update(self, instance, validated_data):
        instance.category = validated_data.get("category", instance.category)
        instance.mbti_tags = validated_data.get("mbti_tags", instance.mbti_tags)
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)

        try:
            images_data = self.context.get("request").data.pop("images")
        except:
            images_data = None

        if images_data is not None:
            image_instance_list = []
            instance.postimage_set.all().delete()
            for image_data in images_data:
                image = PostImage.objects.get_or_create(image=image_data, post=instance)
                image_instance_list.append(image)

        instance.save()
        return instance

    def to_representation(self, instance):
        return PostSerializer(instance, context=self.context).data


class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer()
    number_of_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = PostReply
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
        number_of_likes = instance.postreplylike_set.count()
        return number_of_likes

    def get_is_liked(self, instance):
        reply_like = instance.postreplylike_set.filter(
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
        model = PostComment
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
        number_of_likes = instance.postcommentlike_set.count()
        return number_of_likes

    def get_is_liked(self, instance):
        comment_like = instance.postcommentlike_set.filter(
            user=self.context.get("request").user.pk
        )
        if comment_like:
            return True
        else:
            return False


class CommentCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = PostComment
        fields = ("content", "image")


class CommentUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = PostComment
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
        model = PostReply
        fields = ("content", "image")


class ReplyUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = PostReply
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


class PostLikeSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = PostLike
        fields = ("likes",)

    def get_likes(self, instance):
        post_pk = self.context.get("request").parser_context.get("kwargs")["pk"]
        post_instance = Post.objects.get(pk=post_pk)
        number_of_likes = post_instance.postlike_set.count()
        if post_instance.postlike_set.all().filter(
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


class PostSaveSerializer(serializers.ModelSerializer):
    saved = serializers.SerializerMethodField()

    class Meta:
        model = SavedPost
        fields = ("saved",)

    def get_saved(self, instance):
        post_pk = self.context.get("request").parser_context.get("kwargs")["pk"]
        post_instance = Post.objects.get(pk=post_pk)
        if post_instance.saved_post_set.all().filter(
            nickname=self.context.get("request").user
        ):
            is_liked = True
        else:
            is_liked = False
        return is_liked


class PostBlockSerializer(serializers.ModelSerializer):
    blocked = serializers.SerializerMethodField()

    class Meta:
        model = BlockedPost
        fields = ("blocked",)

    def get_blocked(self, instance):
        post_pk = self.context.get("request").parser_context.get("kwargs")["pk"]
        post_instance = Post.objects.get(pk=post_pk)
        if post_instance.blockedpost_set.all().filter(
            user=self.context.get("request").user
        ):
            is_blocked = True
        else:
            is_blocked = False
        return is_blocked


class CommentLikeSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = PostCommentLike
        fields = ("likes",)

    def get_likes(self, instance):
        comment_pk = self.context.get("request").parser_context.get("kwargs")["pk"]
        comment_instance = PostComment.objects.get(pk=comment_pk)
        number_of_likes = comment_instance.postcommentlike_set.count()
        if comment_instance.postcommentlike_set.all().filter(
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
        model = PostReplyLike
        fields = ("likes",)

    def get_likes(self, instance):
        reply_pk = self.context.get("request").parser_context.get("kwargs")["pk"]
        reply_instance = PostReply.objects.get(pk=reply_pk)
        number_of_likes = reply_instance.postreplylike_set.count()
        if reply_instance.postreplylike_set.all().filter(
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
