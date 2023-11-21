from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user')
    list_filter = ('from_user', 'to_user')
    search_fields = ('from_user__username', 'to_user__username')
    empty_value_display = '-пусто-'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'sender', 'chat_room', 'pub_date')
    list_filter = ('sender', 'chat_room')
    search_fields = ('text', 'sender__username', 'chat_room__id')
    empty_value_display = '-пусто-'
