import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import SyncConsumer, WebsocketConsumer

from celery.result import AsyncResult

from .models import Message
from .tasks import get_question, analyze_response


class ChatConsumer(WebsocketConsumer):
    question_id = None
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']
        self.total_questions = 0
        self.score = 0

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        if text_data_json['type'] == 'message':
            ChatConsumer.question_id = get_question.delay(self.room_group_name)
            message_data = text_data_json['message']

            message = Message.objects.create(user=self.user, content=message_data)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {'type':'chat_message', 'message': message.content, 'user': message.user.username}
            )

        elif text_data_json['type'] == 'response':
            analyze_response.delay(self.channel_name, text_data_json['value'], ChatConsumer.question_id.get())
            
    
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
            'options': options
        }))

    def score_update(self, event):
        print("DJJHJD")
        response_status = event['correct']
        self.total_questions += 1
        self.score += int(response_status)

        print(f"{self.score}/{self.total_questions}")

        self.send(text_data=json.dumps({
            'type': 'score_update',
            'questions': self.total_questions,
            'correct': self.score
        }))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.send(text_data=json.dumps({
            'from': 'Server',
            'message': f'{self.user.username} has left the room'
        }))
