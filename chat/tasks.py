import requests
import random

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from .models import FlagQuestion

channel_layer = get_channel_layer()

@shared_task
def get_question(group_name):
    resp = requests.get('https://restcountries.com/v3.1/all')
    countries = resp.json()

    options = random.sample(countries, 4)
    correct_option = random.choice(options)

    names = [opt['name']['common'] for opt in options if opt != correct_option]
    correct_name = correct_option['name']['common']

    question_flag = correct_option['flags']['png']

    new_question = FlagQuestion.objects.create(flag_url=question_flag, correct_op=correct_name, incorrect_op1 = names[0], incorrect_op2 = names[1], incorrect_op3 = names[2])
    new_question.save()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "question_message",
            "flag": question_flag,
            "options": [*names, correct_name]
        },
    )
