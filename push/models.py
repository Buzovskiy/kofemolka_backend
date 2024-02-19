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
    ("push_notification_bonus", _("Push notification bonus")),
]


class Message(models.Model):
    type = models.CharField(
        _('Notification type'), max_length=255, choices=MESSAGE_TYPES_CHOICES, default='push_notification')
    title = models.CharField('title', max_length=255)
    body = models.TextField('body',
                            help_text=_('To substitute the bonus amount you should use %.f for integer rounding or '
                                        '%.1f to round to one decimal place'))
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

    def build_push_notification_service_quality_message(self, registration_token):
        return {
            'message': {
                'token': registration_token,
                'data': {'title': self.title, 'body': self.body, 'image': self.get_absolute_image_url}
            }
        }

    def build_push_notification_bonus_for_transaction(self, registration_token, bonuses_amount):
        return {
            'message': {
                'token': registration_token,
                'data': {
                    'title': self.title,
                    'body': self.body % bonuses_amount,
                    'image': self.get_absolute_image_url
                }
            }
        }

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
    """
    The table where push messages are stored
    """
    type = models.CharField(
        _('Notification type'), max_length=255, choices=MESSAGE_TYPES_CHOICES, default='push_notification')
    client = models.ForeignKey('clients.Clients', on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField('title', max_length=255, blank=True, null=True)
    body = models.TextField('body', blank=True, null=True)
    image = models.CharField(_('Image'), max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Date created'), auto_now_add=True)

    def __str__(self):
        return f'{self.client} - {self.title}'

    class Meta:
        verbose_name = _('The history of push messages')
        verbose_name_plural = _('The history of push messages')


class ServiceQualityAnswers(models.Model):
    location = models.ForeignKey(
        'location.Location', verbose_name=_('Location'), on_delete=models.CASCADE, blank=False, null=False)
    client = models.ForeignKey(
        'clients.Clients', verbose_name=_('Client'), on_delete=models.CASCADE, blank=False, null=False)
    id_clean = models.IntegerField(verbose_name=_('Cleanliness and sanitation'), blank=True, null=True)
    id_products_quality = models.IntegerField(verbose_name=_('Products quality'), blank=True, null=True)
    id_service_quality = models.IntegerField(verbose_name=_('Service quality'), blank=True, null=True)
    comment = models.TextField(verbose_name=_('Comment'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Date created'), null=True, auto_now_add=True)

    def __str__(self):
        return f'{self.location} - {self.client}'

    class Meta:
        verbose_name = _('Service quality answer')
        verbose_name_plural = _('Service quality answers')
