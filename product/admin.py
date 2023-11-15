from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Products, BatchTickets


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_id')


@admin.register(BatchTickets)
class BatchTicketsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_id')
