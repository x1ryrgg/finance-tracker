from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'all_money', 'text', 'image')

    list_display = ('id', 'user', 'all_money', 'text', 'post_photo', 'time_create')
    list_display_links = ('id', 'user')
    ordering = ("id", 'user')

    @admin.display(description='Изображение')
    def post_photo(self, file: Profile):
        if file.image:
            return mark_safe(f"<img src='{file.image.url}' width=150>")
        return 'Нет фото'


@admin.register(Objective)
class ObjectAdmin(admin.ModelAdmin):
    fields = ("user", 'object', 'obj_money')

    list_display = ('id', 'user', 'object', 'slug', 'obj_money', 'time_create', 'time_update')
    list_display_links = ('id', 'user')
    ordering = ('id', 'user')


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    fields = ('user', 'hs_money', 'spending', 'comment')

    list_display = ('user', 'hs_money', 'spending', 'comment', 'time_create')
    list_display_links = ('user', 'hs_money')
    ordering = ('id', 'hs_money')
