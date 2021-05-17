from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserAllChats, PrivateChatMessage, UserProfile, GroupChat, GroupChatMessage
from .serializers import UserSerializer, AddorGetListSerializers, PrivateChatMessageSerializer, SerializeUser, \
    GroupChatSerializer, GroupChatMessageSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(
            request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


# for signup
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        obj = serializer.save()
        UserProfile.objects.create(user=obj)


class All(APIView):
    def get(self, request):
        user = User.objects.all()
        userserial = SerializeUser(user, many=True)
        if userserial:
            return Response(userserial.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddorGetList(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        chatlist = UserAllChats.objects.filter(user1=self.request.user) | UserAllChats.objects.filter(
            user2=self.request.user)
        chatlist_serial = AddorGetListSerializers(chatlist, many=True)
        if chatlist_serial:
            return Response(chatlist_serial.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        UserAllChats.objects.create(
            user1=self.request.user,
            user2=User.objects.get(id=id),
        )
        return Response(status=status.HTTP_200_OK)


class AddorGetGroupList(APIView):  # OF CURRENT USER
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        g = self.request.user.groupchat_set.all()
        serial = GroupChatSerializer(g, many=True)
        if serial:
            return Response(serial.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        name = self.request.data.get("name")
        description = self.request.data.get("description")
        g = GroupChat.objects.create(name=name, description=description)
        g.users.add(self.request.user)
        return JsonResponse({"id": str(g.pk)})


@api_view(["PUT"])
def join_group(request, name):
    try:
        g = GroupChat.objects.get(name=name)
        g.users.add(request.user)
        serial = GroupChatSerializer(g)
        return Response(serial.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def leave_group(request, id):
    group = GroupChat.objects.get(id=id)
    if request.user in group.users.all():
        group.users.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_group(request, id):
    group = GroupChat.objects.get(id=id)
    name = request.data.get("name")
    description = request.data.get("description")
    image = request.data.get("image")
    if image is not None:
        group.image = image
    group.name = name
    group.description = description
    group.save()
    return Response(status=status.HTTP_200_OK)


class PrivateChatMessageClass(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        messages = PrivateChatMessage.objects.filter(sender=self.request.user, receiver=User.objects.get(
            id=id)) | PrivateChatMessage.objects.filter(receiver=self.request.user, sender=User.objects.get(id=id))
        messages = reversed(messages)
        messagesSerializer = PrivateChatMessageSerializer(messages, many=True)
        if messagesSerializer:
            return Response(messagesSerializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, id):
        PrivateChatMessage.objects.create(
            sender=self.request.user,
            messageUsername=self.request.user.id,
            receiver=User.objects.get(id=id),
            message=self.request.data.get('message')
        )
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id):
        p = PrivateChatMessage.objects.get(id=id)
        p.delete()
        return Response(status=status.HTTP_200_OK)


class UpdateDetails(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        image = self.request.data
        print(image.get("avatar"))
        print(self.request.user.username)
        uf = self.request.user
        u, _ = UserProfile.objects.get_or_create(user=self.request.user)
        if u:
            if image.get("avatar"):
               u.avatar = image.get("avatar")
               u.save()
            print(image.get("username"))
            uf.username= image.get("username")
            uf.save()
            return Response(status=status.HTTP_200_OK)

    def get(self, request):
        user = User.objects.get(id=self.request.user.id)
        us = SerializeUser(user, context={'request': self.request})
        if us:
            return Response(us.data, status=status.HTTP_200_OK)


class GroupChatMessageList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        gc = GroupChat.objects.get(id=id)
        chat = reversed(GroupChatMessage.objects.filter(group=gc))
        chat_serial = GroupChatMessageSerializer(chat, many=True)
        if chat_serial:
            return Response(chat_serial.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, id):
        gc = GroupChat.objects.get(id=id)
        g = GroupChatMessage(
            sender=self.request.user,
            group=gc,
            message=self.request.data.get("message"))

        g.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id):
        p = GroupChatMessage.objects.get(id=id)
        p.delete()
        return Response(status=status.HTTP_200_OK)


 
