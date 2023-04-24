from django.contrib import admin
from django.utils.html import format_html

from .models import Character


class CharacterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "thumbnail", "thumbnail_preview")
    search_fields = ("name",)

    def thumbnail_preview(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.thumbnail)

    thumbnail_preview.short_description = "Thumbnail"


admin.site.register(Character, CharacterAdmin)
