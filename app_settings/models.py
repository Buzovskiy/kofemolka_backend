from django.db import models
from django.utils.translation import gettext_lazy as _


class PosterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(key='poster_token')


class ProposalsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(key='proposals_telephones_list')


class AppSettings(models.Model):
    title = models.CharField(_('Title'), max_length=255, blank=False, null=False)
    key = models.CharField(_('Key'), max_length=255, blank=False, null=False)
    value = models.CharField(_('Value'), max_length=255, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)

    objects = models.Manager()
    poster_token = PosterManager()
    proposals = ProposalsManager()

    def __str__(self):
        return self.title

    def get_telephones_list(self):
        """
        Example: AppSettings.proposals.get().get_telephones_list()
        :return: list of telephone numbers ['+380986260999', '+34655973999']
        """
        return [s.strip() for s in self.value.split(',')]

    class Meta:
        verbose_name = _('Application settings')
        verbose_name_plural = _('Application settings')
