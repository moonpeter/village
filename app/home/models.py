from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from common.utils import rename_imagefile_to_uuid_for_comment

from posts.models import TimeStampedModel


class CompetitionOfThisWeek(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    closing_date = models.DateTimeField(null=True)
    title = models.TextField(null=False, blank=False)
    content = models.TextField(null=True, blank=True)
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="CompetitionLike",
        related_name="like_competition_set",
    )
    hits = models.IntegerField(default=0)

    class Meta:
        ordering = ("-pk",)

    def __str__(self):
        return f"{self.pk} - {self.title}"


class CompetitionChoice(TimeStampedModel):
    competition = models.ForeignKey(
        CompetitionOfThisWeek, on_delete=models.CASCADE, related_name="choice"
    )
    choice_text = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)
    selected_users_pk = ArrayField(models.IntegerField(), null=True)

    def __str__(self):
        return f"{self.competition.title} : {self.choice_text} : {self.votes}"


class CompetitionLike(TimeStampedModel):
    competition = models.ForeignKey(CompetitionOfThisWeek, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.competition.pk} : {self.user}"


class CompetitionComment(TimeStampedModel):
    competition = models.ForeignKey(CompetitionOfThisWeek, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to=rename_imagefile_to_uuid_for_comment)
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="CompetitionCommentLike",
        related_name="like_competition_comment_set",
    )

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return f"{self.pk} - {self.author} - {self.competition.title} - {self.content}"


class CompetitionCommentLike(TimeStampedModel):
    competition_comment = models.ForeignKey(
        CompetitionComment, on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.competition_comment.id} : {self.user}"


class CompetitionReply(TimeStampedModel):
    competition_comment = models.ForeignKey(
        CompetitionComment, on_delete=models.CASCADE, related_name="reply"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to=rename_imagefile_to_uuid_for_comment)
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="CompetitionReplyLike",
        related_name="like_competition_reply_set",
    )

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return f"{self.pk} - {self.author} - {self.competition_comment.content} - {self.content}"


class CompetitionReplyLike(TimeStampedModel):
    competition_reply = models.ForeignKey(CompetitionReply, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.competition_reply.pk} : {self.user}"
