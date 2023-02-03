import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import SyncConsumer, WebsocketConsumer

from .models import Message
from .tasks import get_question


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name, {'type': 'join_message', 'user': str(self.username)}
        # )
    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_data = text_data_json['message']

        message = Message.objects.create(user=self.user, content=message_data)

        get_question.delay(self.room_group_name)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type':'chat_message', 'message': message.content, 'user': message.user.username}
        )
    
    def chat_message(self, event):
        message = event['message']
        sender = event['user']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'from': sender,
            'message': message
            }))
    
    def question_message(self, event):
        flag_url = event['flag']
        options = event['options']

        self.send(text_data=json.dumps({
            'type': 'question',
            'from': 'Server',
            'flag_url': flag_url,
        }))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.send(text_data=json.dumps({
            'from': 'Server',
            'message': f'{self.user.username} has left the room'
        }))
