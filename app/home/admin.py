from django.contrib import admin
from . import models


@admin.register(models.CompetitionOfThisWeek)
class CompetitionOfThisWeekAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title")
    list_filter = ("modified",)


@admin.register(models.CompetitionChoice)
class CompetitionChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "competition", "choice_text")
    list_filter = ("modified",)
