from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.translation import gettext_lazy as _
from .models import Location, LocationAddress, LocationImage
from .exchange import import_locations


def update_locations_from_api(request):
    try:
        objects_added = 0
        res = import_locations()
        if 'objects_created' in res:
            objects_added = res['objects_created']
        messages.success(request, f'{objects_added} {_("objects added")}')
    except:
        messages.error(request, 'e')
    return HttpResponseRedirect("../")


class LocationAddressInline(admin.TabularInline):
    model = LocationAddress
    extra = 0


class LocationImageInline(admin.TabularInline):
    model = LocationImage
    extra = 0
    readonly_fields = ['image_preview']

    @admin.display(description=_('Image'))
    def image_preview(self, obj):
        return obj.image_preview


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'spot_id', 'spot_name')
    list_display_links = ('spot_name',)
    inlines = [LocationAddressInline, LocationImageInline]
    f_list = [field.name for field in Location._meta.get_fields() if field.name != "id"]
    readonly_fields = ('spot_id',)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update-locations-from-api/', update_locations_from_api),
        ]
        return my_urls + urls
