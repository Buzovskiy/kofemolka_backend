from django.db import models
from django.utils.translation import gettext_lazy as _


class PosterManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(key='poster_token')


class AppSettings(models.Model):
    title = models.CharField(_('Title'), max_length=255, blank=False, null=False)
    key = models.CharField(_('Key'), max_length=255, blank=False, null=False)
    value = models.CharField(_('Value'), max_length=255, blank=False, null=False)
    description = models.TextField(_('Description'), blank=True, null=True)

    objects = models.Manager()
    poster_token = PosterManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Application settings')
        verbose_name_plural = _('Application settings')
