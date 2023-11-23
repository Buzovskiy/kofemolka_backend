from django.contrib import admin
from .models import DeliveryType


@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title',)

