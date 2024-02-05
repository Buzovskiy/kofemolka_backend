from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PushConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'push'
    verbose_name = _('Sending push notifications')
