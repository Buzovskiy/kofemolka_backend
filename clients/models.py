from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from sms.turbosms import send_sms
from app_settings.models import AppSettings


class Clients(models.Model):
    client_id = models.CharField(_('Client id'), null=False, blank=False, max_length=255, unique=True)
    firstname = models.CharField(_('First name'), null=False, blank=False, max_length=255)
    lastname = models.CharField(_('Last name'), null=False, blank=False, max_length=255)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


class Comment(models.Model):
    comment = models.TextField(_('Comment'), null=False, blank=False)
    rating = models.IntegerField(_('Rating'), null=True, blank=True)
    client = models.ForeignKey(Clients, verbose_name=_('Client'), on_delete=models.CASCADE)
    approved = models.BooleanField(_('Approved'), default=False)
    response = models.TextField(_('Response'), null=True, blank=True)

    def __str__(self):
        return self.comment[:50]+'...' if len(self.comment) > 50 else self.comment

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class Complaints(models.Model):
    complaint = models.TextField(_('Complaints and suggestions'), null=False, blank=False)

    def __str__(self):
        return self.complaint[:50]+'...' if len(self.complaint) > 50 else self.complaint

    class Meta:
        verbose_name = _('Complaints and suggestions')
        verbose_name_plural = _('Complaints and suggestions')


@receiver(post_save, sender=Complaints)
def post_save_send_sms(sender, instance, *args, **kwargs):
    """When we save Complaints instance send sms"""
    try:
        complaints_settings = AppSettings.complaints.get()
        telephone_numbers_list = complaints_settings.get_telephones_list()
        if len(telephone_numbers_list) > 0:
            send_sms(message=instance.__str__(), recipients=telephone_numbers_list)
    except (AppSettings.DoesNotExist, AttributeError):
        pass
