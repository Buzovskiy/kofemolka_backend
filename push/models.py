import os
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.conf import settings

from kofemolka_backend.utils import post_delete_image, pre_save_image


class PushGroups(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    clients = models.ManyToManyField('clients.Clients')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Push notifications group')
        verbose_name_plural = _('Push notifications groups')


MESSAGE_TYPES_CHOICES = [
    ("push_notification", _("Push notification")),
    ("push_notification_service_quality", _("Push notification service quality")),
    ("push_notification_bonus", _("Push notification service bonus")),
]


class Message(models.Model):
    type = models.CharField(
        _('Notification type'), max_length=255, choices=MESSAGE_TYPES_CHOICES, default='push_notification')
    title = models.CharField('title', max_length=255)
    body = models.TextField('body')
    client = models.ForeignKey(
        'clients.Clients', verbose_name=_('Client'), on_delete=models.CASCADE, blank=True, null=True)
    push_group = models.ForeignKey(
        'push.PushGroups', verbose_name=_('Push notifications group'), on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField('image', upload_to='push-message/', blank=True, null=True)


    @property
    def get_absolute_image_url(self):
        try:
            return "{0}{1}".format(settings.BASE_URL, self.image.url)
        except ValueError:
            return ''

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{url}" height="200px" />'.format(url=self.image.url))
        return ""

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Push message')
        verbose_name_plural = _('Push messages')


@receiver(post_delete, sender=Message)
def delete_image(sender, instance, *args, **kwargs):
    post_delete_image(sender, instance, field_name='image', *args, **kwargs)


@receiver(pre_save, sender=Message)
def save_image(sender, instance, *args, **kwargs):
    pre_save_image(sender, instance, field_name='image', *args, **kwargs)


class MessageClient(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, blank=False, null=False)
    client = models.ForeignKey('clients.Clients', on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(verbose_name=_('Date created'), auto_now_add=True)

    def __str__(self):
        return f'{self.message} - {self.client}'

    class Meta:
        unique_together = [['message', 'client']]
