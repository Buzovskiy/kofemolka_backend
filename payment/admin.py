from django.contrib import admin
from .models import PaymentType


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title',)

