from django.contrib import admin
from django.utils.safestring import mark_safe

from core import models


@admin.register(models.UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = (
        'user',
        'full_name',
        'get_avatar',
    )
    search_fields = ('full_name',)

    def get_avatar(self, obj: models.UserProfile) -> None:
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="60" height="60" />')

    get_avatar.short_description = 'Avatar'
