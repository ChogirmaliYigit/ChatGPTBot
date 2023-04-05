from django.contrib import admin
from main.views import ChatDetail, ChatList
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/<int:user_id>/', ChatList.as_view(), name='chat_list'),
    path('messages/<int:chat_id>/', ChatDetail.as_view(), name='message_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)