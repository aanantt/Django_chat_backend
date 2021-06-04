from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('api/login/', views.CustomObtainAuthToken.as_view(), name='login'),
    path('api/signup/', views.UserCreateAPIView().as_view(), name='signup-api'),
    path('api/all/chats/', views.AddorGetList().as_view(), name='user-chats'),
    path('api/all/groups/', views.AddorGetGroupList().as_view(), name='user-group'),
    path('api/all/', views.All().as_view(), name='allchats'),
    path('api/user/', views.UpdateDetails().as_view(), name='updateprofile'),
    path('api/leave/group/<int:id>/', views.leave_group, name='leave-group'),
    path('api/join/group/<str:name>/', views.join_group, name='join-group'),
    path('api/update/group/<int:id>/', views.update_group, name='update-group'),
    path('api/group/chat/<int:id>/',
         views.GroupChatMessageList().as_view(), name='chat-group'),
    path('all/chats/message/<str:id>/',
         views.PrivateChatMessageClass().as_view(), name='postchats'),
]
