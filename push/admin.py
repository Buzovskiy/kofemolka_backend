from django.contrib import admin
from .models import PushGroups, Message, MessageClient
from django.utils.translation import gettext_lazy as _


@admin.register(PushGroups)
class PushGroupsAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'push_group', 'type']
    readonly_fields = ['image_url', 'image_preview']

    @admin.display(description=_('Image'))
    def image_preview(self, obj):
        return obj.image_preview

    @admin.display(description=_('Image url'))
    def image_url(self, obj):
        return obj.get_absolute_image_url


@admin.register(MessageClient)
class MessageClientAdmin(admin.ModelAdmin):
    list_display = ['message', 'client', 'created_at']
    readonly_fields = ['created_at']
