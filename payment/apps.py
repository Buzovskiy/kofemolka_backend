from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
    verbose_name = _('Payment type')
    verbose_name_plural = _('Payment types')
