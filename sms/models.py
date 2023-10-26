import re

from django.core.exceptions import ValidationError
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


def validate_phone_is_ukrainian(value):
    pattern = re.compile(r"^380\d{9}$")
    result = pattern.match(value)
    if result is None:
        raise ValidationError(
            _("%(value)s does not correspond to format 380XXXXXXXXX"),
            params={"value": value},
        )


class SmsCodes(models.Model):
    phone_number = models.CharField(
        _('Phone number'),
        max_length=255,
        null=False,
        blank=False,
        validators=[validate_phone_is_ukrainian]
    )
    sms_code = models.CharField(_('Sms code'), max_length=255, null=False, blank=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    verified = models.BooleanField(_('Verified'), default=False)

    def __str__(self):
        return f'{self.phone_number}'

    class Meta:
        verbose_name = _('Sms code')
        verbose_name_plural = _('Sms codes')
