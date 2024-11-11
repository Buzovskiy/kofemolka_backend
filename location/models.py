import os
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.conf import settings

from kofemolka_backend.utils import post_delete_image, pre_save_image


class Location(models.Model):
    spot_id = models.CharField(_('Location id'), null=False, blank=False, max_length=255, unique=True)
    name = models.CharField(_('Name in application'), null=False, blank=True, max_length=255)
    spot_name = models.CharField(_('Location name'), null=False, blank=True, max_length=255)
    spot_address = models.CharField(_('Location address'), null=False, blank=True, max_length=255)
    region_id = models.CharField(_('Region id'), null=False, blank=True, max_length=255)
    lat = models.CharField(_('Latitude'), null=False, blank=True, max_length=255)
    lng = models.CharField(_('longitude'), null=False, blank=True, max_length=255)
    wayforpay_key = models.CharField(_('Wayforpay key'), null=True, blank=True, max_length=255)
    wayforpay_account = models.CharField(_('Wayforpay account'), null=True, blank=True, max_length=255)

    def __str__(self):
        return self.spot_name

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')


class LocationAddress(models.Model):
    address = models.CharField(_('Shipping address'), null=False, blank=False, max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = _('Shipping address')
        verbose_name_plural = _('Shipping addresses')


class LocationImage(models.Model):
    image = models.ImageField(_('Image'), upload_to="location/", blank=False, null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

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

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Location mage')
        verbose_name_plural = _('Location images')


@receiver(post_delete, sender=LocationImage)
def delete_image(sender, instance, *args, **kwargs):
    post_delete_image(sender, instance, field_name='image', *args, **kwargs)


@receiver(pre_save, sender=LocationImage)
def save_image(sender, instance, *args, **kwargs):
    pre_save_image(sender, instance, field_name='image', *args, **kwargs)
