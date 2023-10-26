from django.contrib import admin
from sms.models import Setting, SmsCodes


@admin.register(Setting)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('sms_signature', 'active')


@admin.register(SmsCodes)
class SmsCodesAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'sms_code', 'created', 'verified')
    readonly_fields = ('created',)
    fields = ('phone_number', 'sms_code', 'created', 'verified')
