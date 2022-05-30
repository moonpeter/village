from pyexpat import model
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from home.models import CompetitionOfThisWeek

from posts.models import Post, TimeStampedModel
from common.utils import mbti_itmes


# Create your models here.
class User(AbstractUser):
    token = models.TextField(default="")
    email = models.EmailField(max_length=254, null=False, blank=False, unique=True)
    nickname = models.CharField(max_length=50, null=False, blank=False)

    # mbti_type에 대해서 각 인덱스의 값으로 유저 객체 생성 시에 자동으로 저장할 수 있도록 수정 필요
    mbti_type = models.CharField(max_length=4, choices=mbti_itmes)

    mbti_index_items_0 = [("I", "I"), ("E", "E")]
    mbti_index_items_1 = [("N", "N"), ("S", "S")]
    mbti_index_items_2 = [("F", "F"), ("T", "T")]
    mbti_index_items_3 = [("P", "P"), ("J", "J")]
    mbti_index_0 = models.CharField(
        max_length=1, choices=mbti_index_items_0, default=""
    )
    mbti_index_1 = models.CharField(
        max_length=1, choices=mbti_index_items_1, default=""
    )
    mbti_index_2 = models.CharField(
        max_length=1, choices=mbti_index_items_2, default=""
    )
    mbti_index_3 = models.CharField(
        max_length=1, choices=mbti_index_items_3, default=""
    )

    birth_date = models.DateField(blank=True, null=True)
    gender_items = [
        ("M", "male"),
        ("F", "female"),
        ("N", "none"),
    ]
    gender = models.CharField(max_length=1, choices=gender_items, default="N")
    saved_posts = models.ManyToManyField(
        Post, through="SavedPost", related_name="saved_post_set"
    )
    saved_competition = models.ManyToManyField(
        CompetitionOfThisWeek,
        through="SavedCompetition",
        related_name="saved_competition_set",
    )

    def __str__(self) -> str:
        return self.nickname


class SavedPost(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.id} : {self.user}"


class SavedCompetition(TimeStampedModel):
    competition = models.ForeignKey(CompetitionOfThisWeek, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.id} : {self.user}"


class BlockedPost(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.id} : {self.user}"
