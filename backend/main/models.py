from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=250)
    username = models.CharField(max_length=250, null=True, blank=True)
    telegram_id = models.PositiveBigIntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Telegram User'
        db_table = 'users'

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chats'

class Message(models.Model):
    USER = 'user'
    ASSISTANT = 'assistant'
    TYPES = (
        (USER, 'User'),
        (ASSISTANT, 'Assistant')
    )
    message = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT)
    type = models.CharField(max_length=20, choices=TYPES, default=USER)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
