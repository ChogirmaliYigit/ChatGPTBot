from django.contrib import admin
from .models import User, Chat, Message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'telegram_id')
    fields = ('full_name', 'username', 'telegram_id')
    search_fields = ('full_name', 'username', 'telegram_id')
    list_filter = ('created', )

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    fields = ('title', 'user')
    search_fields = ('title', )
    list_filter = ('user', 'created')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('type', 'message', 'chat')
    fields = ('type', 'message', 'chat')
    search_fields = ('message', )
    list_filter = ('type', 'chat', 'created')
