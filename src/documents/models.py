from django.conf import settings
from django.db import models

# Create your models here.

User = settings.AUTH_USER_MODEL # -> "auth.User"

class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(default="Title")
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # db auto update this field to when it's created
    updated_at  = models.DateTimeField(auto_now=True) # db auto update this field to when it's updated
