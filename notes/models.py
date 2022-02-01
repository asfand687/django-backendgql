from django.db import models

from django.db import models
from users.models import CustomUser
from django.conf import settings


# Create your models here.


class Note(models.Model):
    body = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='notes', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['created']
