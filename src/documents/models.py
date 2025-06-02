from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

User = settings.AUTH_USER_MODEL # -> "auth.User"

# ORM
class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # owner_id = models.IntegerField() -> user.id
    title = models.CharField(default="Title")
    content = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    active_at = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # db auto update this field to when it's created
    updated_at  = models.DateTimeField(auto_now=True) # db auto update this field to when it's updated

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if self.active and self.active_at is None:
            self.active_at = timezone.now()
        else:
            self.active_at = None
        super().save(*args, **kwargs)
