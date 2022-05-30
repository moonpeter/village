from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from common.utils import mbti_itmes
from common.utils import rename_imagefile_to_uuid, rename_imagefile_to_uuid_for_comment


class TimeStampedModel(models.Model):
    """
    'created'와 'modified' 필드를 자동으로 업데이트 해 주는
    추상화 기반 클래스 모델.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category_list = [
        ("ct001", "일상"),
        ("ct002", "취미"),
        ("ct003", "연애"),
        ("ct004", "고민상담"),
        ("ct005", "쇼핑"),
        ("ct006", "재테크"),
        ("ct007", "친구"),
        ("ct008", "여행"),
        ("ct009", "다이어트"),
        ("ct010", "질문"),
    ]
    category = ArrayField(
        models.CharField(max_length=20, choices=category_list), null=False, blank=False
    )
    mbti_tags = ArrayField(
        models.CharField(max_length=4, choices=mbti_itmes),
        null=False,
        blank=False,
    )
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField(max_length=500, blank=True)
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="PostLike", related_name="like_post_set"
    )
    hits = models.IntegerField(default=0)

    class Meta:
        ordering = ("-pk",)

    def __str__(self):
        return f"{self.pk} - {self.author} : {self.title}"


class PostImage(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=rename_imagefile_to_uuid)

    def __str__(self):
        return f"{self.post.title} : {self.image}"


class PostLike(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.id} : {self.user}"


class PostComment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to=rename_imagefile_to_uuid_for_comment)
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="PostCommentLike",
        related_name="like_post_comment_set",
    )

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return f"{self.pk} - {self.author} - {self.post.title} - {self.content}"


class PostCommentLike(TimeStampedModel):
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post_comment.id} : {self.user}"


class PostReply(TimeStampedModel):
    post_comment = models.ForeignKey(
        PostComment, on_delete=models.CASCADE, related_name="reply"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to=rename_imagefile_to_uuid_for_comment)
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="PostReplyLike",
        related_name="like_post_reply_set",
    )

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return (
            f"{self.pk} - {self.author} - {self.post_comment.content} - {self.content}"
        )


class PostReplyLike(TimeStampedModel):
    post_reply = models.ForeignKey(PostReply, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post_reply.id} : {self.user}"


class PollQuestion(TimeStampedModel):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.post.title} : {self.title}"


class PollChoice(models.Model):
    question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    selected_users_pk = ArrayField(models.IntegerField(), null=True)

    def __str__(self):
        return f"{self.question.title} : {self.choice_text} : {self.votes}"
