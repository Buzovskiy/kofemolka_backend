from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Type, Products


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type')

    @admin.display(description=_('Type'))
    def type(self, obj):
        return obj.type


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_id', 'type')
    list_filter = ["type"]

