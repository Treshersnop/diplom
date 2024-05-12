from django.contrib import admin

from chat import models


@admin.register(models.Room)
class Room(admin.ModelAdmin):
    list_display = ('name', 'is_group')
    search_fields = ('name',)


@admin.register(models.Message)
class Message(admin.ModelAdmin):
    list_display = ('description', 'room',)


@admin.register(models.MessageFile)
class MessageFile(admin.ModelAdmin):
    list_display = ('name', 'message',)