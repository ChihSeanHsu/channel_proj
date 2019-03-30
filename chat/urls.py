from django.urls import path, re_path

from chat.views import ChatRoom

app_name = 'chat'

urlpatterns = [
    path('', ChatRoom.as_view(), name='char_room')
]
