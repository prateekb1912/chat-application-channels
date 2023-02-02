from django.contrib import admin
from .models import Message, FlagQuestion

# Register your models here.
admin.site.register(Message)
admin.site.register(FlagQuestion)