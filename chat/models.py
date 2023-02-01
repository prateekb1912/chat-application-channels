from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Message(models.Model):
    content = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}: {self.content}'
