from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserAllChats, PrivateChatMessage, GroupChat, GroupChatMessage


class SerializeUser(serializers.ModelSerializer):
    avatar = serializers.CharField(source="userprofile.avatar")

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.username = validated_data['username']
        instance.save()
        return instance


class AddorGetListSerializers(serializers.ModelSerializer):
    chatwith = SerializeUser()

    class Meta:
        model = UserAllChats
        fields = '__all__'


class PrivateChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChatMessage
        fields = "__all__"


class GroupChatSerializer(serializers.ModelSerializer):
    users = SerializeUser(read_only=True, many=True)

    class Meta:
        model = GroupChat
        fields = ('id', 'image', 'name', 'description', 'users')


class GroupChatMessageSerializer(serializers.ModelSerializer):
    sender = SerializeUser()

    class Meta:
        model = GroupChatMessage
        fields = ('id', 'sender', 'message', 'isfile', 'file')
