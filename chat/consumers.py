# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

import json
import logging

logger = logging.getLogger('django')


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # get name from ws url args
        self.name = self.scope['url_route']['kwargs']['name']
        logger.debug('connect')
        # Join group group_add('group_name', 'channel_name')
        await self.channel_layer.group_add(
            'lobby',
            self.channel_name
        )

        await self.accept()
        await self.group_send(f'{self.name} join the room.')

    async def disconnect(self, close_code):
        # Leave group group_discard('group_name', 'channel_name')
        await self.channel_layer.group_discard(
            'lobby',
            self.channel_name
        )
        await self.group_send(f'{self.name} left the room.')

    # Receive message from WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = self.name + ': ' + text_data_json['message']
        logger.debug('send')

        # Send message to room group
        await self.group_send(message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def group_send(self, msg, group='lobby', type_='chat_message'):
        # group_send('group_name', {'type': type, **kwargs})
        # type means what function you want to do
        await self.channel_layer.group_send(
            group,
            {
                'type': type_,
                'message': msg
            }
        )
