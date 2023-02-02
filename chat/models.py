from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Message(models.Model):
    content = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}: {self.content}'

class FlagQuestion(models.Model):
    flag_url = models.URLField()
    correct_op = models.CharField(max_length=64)
    incorrect_op1 = models.CharField(max_length=64)
    incorrect_op2 = models.CharField(max_length=64)
    incorrect_op3 = models.CharField(max_length=64)
