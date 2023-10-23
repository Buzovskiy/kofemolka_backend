from django.contrib import admin
from sms.models import Setting


@admin.register(Setting)
class SettingsAdmin(admin.ModelAdmin):
    pass
