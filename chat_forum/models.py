# chat_forum/models.py

from django.db import models
from django.utils.translation import gettext as _

from two_factor_auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=199, verbose_name=_('Topic Name'))

    def __str__(self):
        return self.name
    

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('Host'))
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, verbose_name=_('Topic'))
    name = models.CharField(max_length=199, verbose_name=_('Room Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Room Description'))
    participants = models.ManyToManyField(User, related_name='participants', blank=True, verbose_name=_('Participants'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Last Updated'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_('Room'))
    body = models.TextField(verbose_name=_('Message Body'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Last Updated'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.body[0:59]
    