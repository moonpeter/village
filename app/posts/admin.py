from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author")
    list_filter = ("modified",)


@admin.register(models.PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "content")
    list_filter = ("modified",)


@admin.register(models.PostReply)
class PostReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "post_comment", "author", "content")
    list_filter = ("modified",)
