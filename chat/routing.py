from django.urls import re_path, path
from . import consumers
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:me>/<str:notme>/', consumers.PrivateChatConsumer.as_asgi()),
    path('ws/delete/<str:me>/<str:notme>/', consumers.PrivateMessageDeletedConsumer.as_asgi()),
    path('ws/status/<str:me>/<str:notme>/', consumers.PrivateStatusConsumer.as_asgi()),
    path('ws/group/<str:me>/<str:groupid>/', consumers.GroupChatConsumer.as_asgi()),
    path('ws/group/deleted/<str:me>/<str:groupid>/', consumers.GroupDeletedConsumer.as_asgi()),
    path('ws/group/status/<str:me>/<str:groupid>/', consumers.GroupStatusConsumer.as_asgi()),
]
# sudo docker run -p 6379:6379 -d redis:5
