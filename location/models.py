from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe


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
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{url}" width="200px" />'.format(url=self.image.url))
        return ""

    def __str__(self):
        return self.spot_name

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')


class LocationAddress(models.Model):
    address = models.CharField(_('Address'), null=False, blank=False, max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
