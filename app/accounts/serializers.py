from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import exceptions, serializers
from rest_framework import serializers
from requests.exceptions import ConnectionError, HTTPError

from django.db import transaction

from .exceptions import BAD_REQUEST, PreconditionFailed, INTERNAL_SERVER_ERROR

from posts.models import Post, PostComment, PostImage

import random


class CustomSocialSignupSigninSerializer(SocialLoginSerializer):
    # 공통
    access_token = serializers.CharField()
    provider = serializers.ChoiceField(
        choices=[
            ("kakao", "kakao"),
            ("apple", "apple"),
            ("naver", "naver"),
            ("google", "google"),
        ],
    )
    nickname = serializers.CharField()
    birth_date = serializers.DateField()
    gender = serializers.ChoiceField(
        choices=[
            ("M", "male"),
            ("F", "female"),
            ("N", "none"),
        ],
    )
    mbti_items = [
        # 분석형
        ("INTJ", "INTJ"),
        ("INTP", "INTP"),
        ("ENTJ", "ENTJ"),
        ("ENTP", "ENTP"),
        # 외교형
        ("INFJ", "INFJ"),
        ("INFP", "INFP"),
        ("ENFJ", "ENFJ"),
        ("ENFP", "ENFP"),
        # 관리형
        ("ISTJ", "ISTJ"),
        ("ISFJ", "ISFJ"),
        ("ESTJ", "ESTJ"),
        ("ESFJ", "ESFJ"),
        # 탐험가형
        ("ISTP", "ISTP"),
        ("ISFP", "ISFP"),
        ("ESTP", "ESTP"),
        ("ESFP", "ESFP"),
    ]
    mbti_type = serializers.ChoiceField(choices=mbti_items)
    mbti_index_items_0 = [("I", "I"), ("E", "E")]
    mbti_index_items_1 = [("N", "N"), ("S", "S")]
    mbti_index_items_2 = [("F", "F"), ("T", "T")]
    mbti_index_items_3 = [("P", "P"), ("J", "J")]
    mbti_index_0 = serializers.ChoiceField(choices=mbti_index_items_0)
    mbti_index_1 = serializers.ChoiceField(choices=mbti_index_items_1)
    mbti_index_2 = serializers.ChoiceField(choices=mbti_index_items_2)
    mbti_index_3 = serializers.ChoiceField(choices=mbti_index_items_3)

    def get_social_login(self, adapter, app, token, response):
        request = self._get_request()
        social_login, user = adapter.complete_login(
            request, app, token, response=response
        )
        social_login.token = token
        return (social_login, user)

    def validate(self, attrs):
        view = self.context.get("view")
        request = self._get_request()
        adapter_class = getattr(view, "adapter_class", None)
        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)

        access_token = attrs.get("access_token")
        if access_token:
            token_to_parse = {"access_token": access_token}
            token = access_token
        else:
            raise BAD_REQUEST(
                {
                    "code": "VAE0001",
                    "error": "Incorrect input. access_token is required.",
                }
            )

        social_token = adapter.parse_token(token_to_parse)
        social_token.app = app

        try:
            login, user = self.get_social_login(adapter, app, social_token, token)
            with transaction.atomic():
                if not user:
                    user = login.user
                    user.provider = attrs["provider"]
                    user.username = user.email.split("@")[0]
                    user.email = login.user.email

                    while True:
                        try:
                            get_user_model().objects.get(username=user.username)
                            user.username = user.username + str(random.randint(1, 99))
                        except get_user_model().DoesNotExist:
                            break
                    user.save()

                user.token = attrs["access_token"]
                user.nickname = attrs["nickname"]
                user.birth_date = attrs["birth_date"]
                user.gender = attrs["gender"]
                user.mbti_type = attrs["mbti_type"]
                user.mbti_index_0 = attrs["mbti_index_0"]
                user.mbti_index_1 = attrs["mbti_index_1"]
                user.mbti_index_2 = attrs["mbti_index_2"]
                user.mbti_index_3 = attrs["mbti_index_3"]
                user.save()

        except BAD_REQUEST:
            raise BAD_REQUEST(
                {
                    "code": "VAE0002",
                    "error": "registered email error",
                }
            )
        except PreconditionFailed as e:
            if str(e) == "-1":
                raise PreconditionFailed(
                    {
                        "code": "VAE0003",
                        "error": "missing email information in token",
                    }
                )
        except exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationFailed(
                {
                    "code": "VAE0004",
                    "error": "social token authentication was failed",
                }
            )
        except (HTTPError, ConnectionError) as e:
            raise INTERNAL_SERVER_ERROR(
                {
                    "code": "VAE0000",
                    "error": "internal server error",
                }
            )

        attrs["user"] = user
        return attrs


class CustomSocialLoginSerializer(SocialLoginSerializer):
    provider = serializers.ChoiceField(
        choices=[
            ("kakao", "kakao"),
            ("apple", "apple"),
            ("naver", "naver"),
            ("google", "google"),
        ],
    )

    def get_social_login(self, adapter, app, token, response):
        request = self._get_request()
        login, user = adapter.complete_login(request, app, token, response=response)
        return (login, user)

    def validate(self, attrs):
        view = self.context.get("view")
        request = self._get_request()
        adapter_class = getattr(view, "adapter_class", None)
        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)

        access_token = attrs.get("access_token")
        if access_token:
            token_to_parse = {"access_token": access_token}
            token = access_token
        else:
            raise BAD_REQUEST(
                {
                    "code": "VAE0001",
                    "error": "Incorrect input. access_token is required.",
                }
            )
        social_token = adapter.parse_token(token_to_parse)
        social_token.app = app
        try:
            login, user = self.get_social_login(adapter, app, social_token, token)
            user.email = login.user.email
            user.token = attrs["access_token"]
            user.save()

        except PreconditionFailed as e:
            error = str(e)
            if error == "-1":
                raise PreconditionFailed(
                    {
                        "code": "VAE0003",
                        "error": "missing email information in token",
                    }
                )
            elif error == "0":
                raise PreconditionFailed(
                    {
                        "code": "VAE0007",
                        "error": "unregistered user",
                    }
                )
        except exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationFailed(
                {
                    "code": "VAE0004",
                    "error": "social token authentication was failed",
                }
            )
        except (HTTPError, ConnectionError) as e:
            raise INTERNAL_SERVER_ERROR(
                {
                    "code": "VAE0000",
                    "error": "internal server error",
                }
            )
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    mbti_indices = serializers.SerializerMethodField()

    def get_mbti_indices(self, instance):
        mbti_indices = {
            "mbti_index_0": instance.mbti_index_0,
            "mbti_index_1": instance.mbti_index_1,
            "mbti_index_2": instance.mbti_index_2,
            "mbti_index_3": instance.mbti_index_3,
        }
        return mbti_indices

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "nickname", "birth_date", "gender", "mbti_indices")


class UserPostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    image_url = serializers.SerializerMethodField()
    poll = serializers.SerializerMethodField()
    number_of_comments_and_reply = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
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

    def get_is_liked(self, instance):
        post_like = instance.postlike_set.filter(
            user=self.context.get("request").user.pk
        )
        if post_like:
            return True
        else:
            return False

    def get_number_of_likes(self, instance):
        number_of_likes = instance.postlike_set.count()
        return number_of_likes


class UserSelectedPostListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    image_url = serializers.SerializerMethodField()
    poll = serializers.SerializerMethodField()
    number_of_comments_and_reply = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
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
            "is_saved",
            "is_blocked",
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

    def get_is_liked(self, instance):
        post_like = instance.postlike_set.filter(
            user=self.context.get("request").user.pk
        )
        if post_like:
            return True
        else:
            return False

    def get_is_saved(self, instance):
        saved_post = instance.saved_post_set.filter(
            nickname=self.context.get("request").user
        )
        if saved_post:
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


class UserInformationSerializer(serializers.ModelSerializer):
    mbti_indices = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    def get_mbti_indices(self, instance):
        mbti_indices = {
            "mbti_index_0": instance.mbti_index_0,
            "mbti_index_1": instance.mbti_index_1,
            "mbti_index_2": instance.mbti_index_2,
            "mbti_index_3": instance.mbti_index_3,
        }
        return mbti_indices

    def get_posts(self, instance):
        posts = instance.post_set.all()
        try:
            last_id = self.context.get("request").query_params["last-id"]
            posts = posts.filter(pk__lt=last_id)
        except MultiValueDictKeyError:
            pass
        posts = posts.prefetch_related(
            "postimage_set",
            "pollquestion__pollchoice_set",
            "postcomment_set",
            "postcomment_set__reply",
            "postlike_set",
            "postlike_set__user",
        )
        posts = posts[:10]
        return UserPostSerializer(
            posts, read_only=True, many=True, context=self.context
        ).data

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "nickname",
            "birth_date",
            "gender",
            "mbti_indices",
            "posts",
        )
