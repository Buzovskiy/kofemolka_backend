from django.db import models
from django.utils.translation import gettext_lazy as _


class Setting(models.Model):
    sms_signature = models.CharField(_('SMS_SIGNATURE'), max_length=255, null=False, blank=False)
    sms_token = models.CharField(_('SMS_TOKEN'), max_length=255, null=False, blank=False)
    active = models.BooleanField(_('active'), default=True)

    def __str__(self):
        return self.sms_signature

    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')
