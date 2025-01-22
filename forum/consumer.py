from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from datetime import datetime
from .models import ChatRoom, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, message):
        # Save the message to the database
        try:
            room = ChatRoom.objects.get(name=self.room_name)
            user = self.scope['user']
            ChatMessage.objects.create(
                room=room,
                author=user,
                content=message
            )
        except ChatRoom.DoesNotExist:
            pass  # Handle room not existing if necessary

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        username = self.scope['user'].username if self.scope['user'].is_authenticated else 'Anonymous'

        # Save the message to the database
        await self.save_message(message)

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
        )

    async def chat_message(self, event):
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))
