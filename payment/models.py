from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentType(models.Model):
    title = models.CharField(_('Title'), null=False, blank=False, max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Payment type')
        verbose_name_plural = _('Payment types')
