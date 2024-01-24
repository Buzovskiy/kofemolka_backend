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
    registration_token = models.CharField(
        _('Registration token'),
        null=True,
        blank=True,
        max_length=255,
        help_text=_('Is used by Firebase for sending push notifications')
    )

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


class Comment(models.Model):
    comment = models.TextField(_('Feedbacks and complaints'), null=False, blank=False)
    rating = models.IntegerField(_('Rating'), null=True, blank=True)
    client = models.ForeignKey(Clients, verbose_name=_('Client'), on_delete=models.CASCADE)
    location = models.ForeignKey('location.Location', on_delete=models.CASCADE, null=False)
    approved = models.BooleanField(_('Approved'), default=False)
    response = models.TextField(_('Response'), null=True, blank=True)

    def __str__(self):
        return self.comment[:50]+'...' if len(self.comment) > 50 else self.comment

    class Meta:
        verbose_name = _('Feedbacks and complaints')
        verbose_name_plural = _('Feedbacks and complaints')


class Proposal(models.Model):
    proposal = models.TextField(_('Proposal'), null=False, blank=False)

    def __str__(self):
        return self.proposal[:50]+'...' if len(self.proposal) > 50 else self.proposal

    class Meta:
        verbose_name = _('Proposal')
        verbose_name_plural = _('Proposals')


@receiver(post_save, sender=Proposal)
def post_save_send_sms(sender, instance, *args, **kwargs):
    """When we save Proposal instance send sms"""
    try:
        proposals_settings = AppSettings.proposals.get()
        telephone_numbers_list = proposals_settings.get_telephones_list()
        if len(telephone_numbers_list) > 0:
            send_sms(message=instance.__str__(), recipients=telephone_numbers_list)
    except (AppSettings.DoesNotExist, AttributeError):
        pass
