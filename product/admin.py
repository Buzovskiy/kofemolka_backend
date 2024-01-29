from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.translation import gettext_lazy as _
from .models import Products, BatchTickets
from .exchange import import_products, import_batchtickets


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_id')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update-products-from-api/', self.update_products_from_api),
            path('send-push/<int:message_id>', self.send_push),
        ]
        return my_urls + urls

    def update_products_from_api(self, request):
        try:
            objects_added = 0
            res = import_products()
            if 'objects_created' in res:
                objects_added = res['objects_created']
            messages.success(request, f'{objects_added} {_("objects added")}')
        except:
            messages.error(request, 'e')
        return HttpResponseRedirect("../")

    def send_push(self, request, message_id):
        from django.urls import reverse
        change_url = reverse("admin:product_products_change", args=(message_id,))
        print('hello')
        return HttpResponseRedirect(change_url)


@admin.register(BatchTickets)
class BatchTicketsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_id')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update-batchtickets-from-api/', self.update_batchtickets_from_api),
        ]
        return my_urls + urls

    def update_batchtickets_from_api(self, request):
        try:
            objects_added = 0
            res = import_batchtickets()
            if 'objects_created' in res:
                objects_added = res['objects_created']
            messages.success(request, f'{objects_added} {_("objects added")}')
        except:
            messages.error(request, 'e')
        return HttpResponseRedirect("../")
