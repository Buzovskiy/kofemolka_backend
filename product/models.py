from django.db import models
from django.utils.translation import gettext_lazy as _


ALIAS_CHOICES = (
    ('products', _('Products')),
    ('batchtickets', _('Batch tickets')),
)


class Type(models.Model):
    title = models.CharField(_('Title'), choices=ALIAS_CHOICES, unique=True, null=False, blank=False)

    @property
    def type(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')


class Products(models.Model):
    product_name = models.CharField(_('Product name'), null=False, blank=False, max_length=255)
    product_id = models.IntegerField(_('External product id'), unique=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    type = models.ForeignKey(Type, verbose_name=_('Type'), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_name} - {self.type}'

    class Meta:
        verbose_name = _('Product or batch ticket')
        verbose_name_plural = _('Products or batch tickets')
