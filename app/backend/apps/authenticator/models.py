from django.db import models

from ..utils.models import ModelBase


class PC2User(ModelBase):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    event_id = models.PositiveSmallIntegerField(unique=True)
    logs = models.TextField()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'