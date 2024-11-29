# chatgpt/models.py

from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class ChatData(models.Model):
    message = models.CharField(max_length=999991, verbose_name=_('Message'))
    response = models.CharField(max_length=999991, verbose_name=_('Response'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    
    class Meta:
        verbose_name = _('Chat Data')
        verbose_name_plural = _('Chat Data Entries')


    def __str__(self):
        return self.message
