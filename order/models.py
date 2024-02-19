from django.db import models
from django.utils.translation import gettext_lazy as _


class Transaction(models.Model):
    transaction_id = models.IntegerField(_('Transaction ID'), unique=True, null=False, blank=False)
    location = models.ForeignKey(
        'location.Location', verbose_name=_('Location ID'), on_delete=models.CASCADE, null=False, blank=False)
    client = models.ForeignKey(
        'clients.Clients', verbose_name=_('Client ID'), on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    push_quality_service_is_sent = models.BooleanField(_('Push quality service is sent'), default=False)

    def __str__(self):
        return f'{self.transaction_id} - {self.location} - {self.client}'
