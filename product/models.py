from django.db import models
from django.utils.translation import gettext_lazy as _


class Products(models.Model):
    product_name = models.CharField(_('Name'), null=False, blank=False, max_length=255)
    product_id = models.IntegerField(_('External id'), unique=True)
    description = models.TextField(_('Description'), null=True, blank=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class BatchTickets(models.Model):
    product_name = models.CharField(_('Name'), null=False, blank=False, max_length=255)
    product_id = models.IntegerField(_('External id'), unique=True)
    description = models.TextField(_('Description'), null=True, blank=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = _('Batch ticket')
        verbose_name_plural = _('Batch tickets')
