from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryType(models.Model):
    title = models.CharField(_('Title'), null=False, blank=False, max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Delivery type')
        verbose_name_plural = _('Delivery types')
