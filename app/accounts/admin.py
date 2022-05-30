from django.contrib import admin
from django.contrib.auth import forms, get_user_model

# Register your models here.


class AdminChangeForm(forms.UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "username"]
    form = AdminChangeForm


admin.site.register(get_user_model(), UserAdmin)
