from django.shortcuts import render, get_object_or_404
from .models import User, Chat, Message
from django.views import View
from django.db.models import Q


class ChatList(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(Q(user_id=user_id) & ~Q(title=None)).order_by('-created')
        return render(request, 'main/chat_list.html', {'chats': chats})


class ChatDetail(View):
    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, pk=chat_id)
        messages = Message.objects.filter(chat=chat)
        return render(request, 'main/chat_detail.html', {'chat': chat, 'messages': messages})
