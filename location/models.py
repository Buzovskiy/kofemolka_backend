import os
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.conf import settings


class Location(models.Model):
    spot_id = models.CharField(_('Location id'), null=False, blank=False, max_length=255, unique=True)
    name = models.CharField(_('Name'), null=False, blank=True, max_length=255)
    spot_name = models.CharField(_('Location name'), null=False, blank=True, max_length=255)
    spot_address = models.CharField(_('Location address'), null=False, blank=True, max_length=255)
    region_id = models.CharField(_('Region id'), null=False, blank=True, max_length=255)
    lat = models.CharField(_('Latitude'), null=False, blank=True, max_length=255)
    lng = models.CharField(_('longitude'), null=False, blank=True, max_length=255)
    image = models.ImageField(_('Image'), upload_to="location/", blank=True, null=False)

    @property
    def get_absolute_image_url(self):
        try:
            return "{0}{1}".format(settings.BASE_URL, self.image.url)
        except ValueError:
            return ''


    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{url}" width="200px" />'.format(url=self.image.url))
        return ""

    def __str__(self):
        return self.spot_name

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')


@receiver(post_delete, sender=Location)
def post_delete_image(sender, instance, *args, **kwargs):
    """When we delete Location instance, delete old image file """
    try:
        instance.image.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Location)
def pre_save_image(sender, instance, *args, **kwargs):
    """When update Location, delete old image file.Instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(pk=instance.pk).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass


class LocationAddress(models.Model):
    address = models.CharField(_('Address'), null=False, blank=False, max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
