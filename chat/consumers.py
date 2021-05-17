import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
# from .models import Message

from .models import PrivateChatMessage, GroupChat, GroupChatMessage


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user1 = self.scope['url_route']['kwargs']['me']
        self.user2 = self.scope['url_route']['kwargs']['notme']
        string = ''
        if self.user1 > self.user2:
            string = f"{self.user1}_{self.user2}"
        else:
            string = f"{self.user2}_{self.user1}"

        self.room_name = string
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"CHANNEL : {self.room_group_name}")

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print("\n\n\n\n\n")
        print(data)
        message = data['message']
        me = self.scope['url_route']['kwargs']['me']
        notme = self.scope['url_route']['kwargs']['notme']
        isfile = data["isfile"]
        format1 = data["name"]
        if isfile:
            some_bytes = bytearray(message)
            message = bytes(some_bytes)

        payload = await self.save_message(message, me, notme, isfile, format1)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': payload.message,
                'sender': me,
                'receiver': notme,
                'id': payload.pk,
                'isfile': payload.isfile,
                'file': str(payload.file)

            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        isfile = event['isfile']
        file = event['file']
        sender = event['sender']
        id = event['id']
        receiver = event['receiver']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'messageUsername': int(str(sender)),
            'sender': sender,
            'receiver': receiver,
            'id': id,
            'file': file,
            'isfile': isfile
        }))

    @sync_to_async
    def save_message(self, message, sender, receiver, isfile, name):
        sen = User.objects.get(id=sender)
        rec = User.objects.get(id=receiver)
        if isfile:
            uploaded_file = ContentFile(message)
            uploaded_file.name = name
            message = PrivateChatMessage.objects.create(
                sender=sen,
                messageUsername=sender,
                receiver=rec,
                isfile=isfile,
                message="media",
                file=uploaded_file)
            print(message.file)
            # message = PrivateChatMessage.objects.get(id )
            return message

        message = PrivateChatMessage.objects.create(
            sender=sen,
            messageUsername=sender,
            receiver=rec,
            isfile=isfile,
            message=message,
        )
        return message


class PrivateStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user1 = self.scope['url_route']['kwargs']['me']
        self.user2 = self.scope['url_route']['kwargs']['notme']
        string = ''
        if self.user1 > self.user2:
            string = f"{self.user1}_{self.user2}"
        else:
            string = f"{self.user2}_{self.user1}"

        self.room_name = string
        self.room_group_name = 'chat_status_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"CHANNEL : {self.room_group_name}")

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)
        status = data['status']
        me = self.scope['url_route']['kwargs']['me']
        notme = self.scope['url_route']['kwargs']['notme']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.status',
                'status': status,
                'sender': me,
                'receiver': notme,

            }
        )

    # Receive message from room group
    async def chat_status(self, event):
        status = event['status']
        sender = event['sender']
        receiver = event['receiver']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'status': status,
            'sender': sender,
            'receiver': receiver,
        }))


class PrivateMessageDeletedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user1 = self.scope['url_route']['kwargs']['me']
        self.user2 = self.scope['url_route']['kwargs']['notme']
        string = ''
        if self.user1 > self.user2:
            string = f"{self.user1}_{self.user2}"
        else:
            string = f"{self.user2}_{self.user1}"

        self.room_name = string
        self.room_group_name = 'chat_deleted_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"CHANNEL : {self.room_group_name}")

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)
        status = data['status']
        me = self.scope['url_route']['kwargs']['me']
        notme = self.scope['url_route']['kwargs']['notme']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.status',
                'status': status,
                'sender': me,
                'receiver': notme,

            }
        )

    # Receive message from room group
    async def chat_status(self, event):
        status = event['status']
        sender = event['sender']
        receiver = event['receiver']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'status': status,
            'sender': sender,
            'receiver': receiver,
        }))


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['url_route']['kwargs']['me']
        self.group = self.scope['url_route']['kwargs']['groupid']
        self.room_name = self.group
        self.room_group_name = 'chat_group_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"CHANNEL : {self.room_group_name}")

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print("\n\n\n\n\n")
        print(data)
        message = data['message']
        me = self.scope['url_route']['kwargs']['me']
        group = self.scope['url_route']['kwargs']['groupid']
        isfile = data["isfile"]
        name = data["name"]
        if isfile:
            some_bytes = bytearray(message)
            message = bytes(some_bytes)

        payload = await self.save_message(message, me, group, isfile, name)
        user = await self.getUser(me)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'group.message',
                'message': payload.message,
                'group': group,
                'userid':user.id,
                'username':user.username,
                'id': payload.pk,
                'isfile': payload.isfile,
                'file': str(payload.file)

            }
        )

    # Receive message from room group
    async def group_message(self, event):
        message = event['message']
        isfile = event['isfile']
        file = event['file']
        userid = event['userid']
        id = event['id']
        username = event['username']
        group = event['group']
        print(id)
        data={
            "id":id,
            "isfile":isfile,
            "file":file,
            "message":message,
            "sender":{
                "id":userid,
                'username':username
             }
             
        }
        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

    @sync_to_async
    def save_message(self, message, sender, group, isfile, name):
        sen = User.objects.get(id=sender)
        group = GroupChat.objects.get(id=group)
        if isfile:
            uploaded_file = ContentFile(message)
            uploaded_file.name = name
            message = GroupChatMessage.objects.create(
                sender=sen,
                group=group,
                isfile=isfile,
                message="media",
                file=uploaded_file
            )
            return message

        message = GroupChatMessage.objects.create(
            sender=sen,
            group=group,
            isfile=isfile,
            message=message,

        )
        return message

    @sync_to_async
    def getUser(self,id):
        user = User.objects.get(id=id)
        return user





class GroupStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['url_route']['kwargs']['me']
        self.group = self.scope['url_route']['kwargs']['groupid']
        self.room_name = self.group
        self.room_group_name = 'chat_group_status_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"CHANNEL : {self.room_group_name}")

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)
        status = data['status']
        sender = self.scope['url_route']['kwargs']['me']
        group = self.scope['url_route']['kwargs']['groupid']
        # Send message to room group

        username = await self.getUsername(sender)

        print(username)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.status',
                'status': status,
                'sender': sender,
                'username': username,
                'group': group,

            }
        )

    @sync_to_async
    def getUsername(self, id):
        username = User.objects.get(id=id).username
        return username

    # Receive message from room group

    async def chat_status(self, event):
        status = event['status']
        sender = event['sender']
        group = event['group']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'status': status,
            'sender': sender,
            'group': group,
            'username': str(username)
        }))


class GroupDeletedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['url_route']['kwargs']['me']
        self.group = self.scope['url_route']['kwargs']['groupid']
        self.room_name = self.group
        self.room_group_name = 'chat_group_deleted_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"CHANNEL : {self.room_group_name}")

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)
        status = data['status']
        sender = self.scope['url_route']['kwargs']['me']
        group = self.scope['url_route']['kwargs']['groupid']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.status',
                'status': status,
                'sender': sender,
                'group': group,

            }
        )

    # Receive message from room group
    async def chat_status(self, event):
        status = event['status']
        sender = event['sender']
        group = event['group']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'status': status,
            'sender': sender,
            'group': group,
        }))
