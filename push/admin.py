from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils.translation import gettext_lazy as _
from .models import PushGroups, Message, MessageClient, ServiceQualityAnswers
from clients.models import Clients
from .sending_push import send_push_by_message_template


@admin.register(MessageClient)
class MessageClientAdmin(admin.ModelAdmin):
    list_display = ('type', 'client', 'title', 'body', 'image_preview', 'created_at')

    @admin.display(description=_('Image'))
    def image_preview(self, obj):
        return obj.image_preview


@admin.register(PushGroups)
class PushGroupsAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        clients_qs = Clients.objects.exclude(registration_token__exact='').exclude(registration_token__isnull=True)
        context['adminform'].form.fields['clients'].queryset = clients_qs
        return super(PushGroupsAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'push_group', 'type']
    readonly_fields = ['image_url', 'image_preview']

    @admin.display(description=_('Image'))
    def image_preview(self, obj):
        return obj.image_preview

    def render_change_form(self, request, context, *args, **kwargs):
        clients_qs = Clients.objects.exclude(registration_token__exact='').exclude(registration_token__isnull=True)
        context['adminform'].form.fields['client'].queryset = clients_qs
        return super(MessageAdmin, self).render_change_form(request, context, *args, **kwargs)

    @admin.display(description=_('Image url'))
    def image_url(self, obj):
        return obj.get_absolute_image_url

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('client-send-push/<int:message_id>', self.client_send_push, name="client-send-push"),
            path('group-send-push/<int:message_id>', self.group_send_push, name="group-send-push"),
        ]
        return my_urls + urls

    def client_send_push(self, request, message_id):
        change_url = reverse("admin:push_message_change", args=(message_id,))
        result = send_push_by_message_template(message_id=message_id, receiver='client')
        try:
            if 'error' in result:
                messages.error(request, result['error'])
            elif 'total' in result and 'success_num' in result:
                info_message = _('%(success_num)d of %(total)d push notifications were sent successfully')
                messages.info(request, info_message % {'success_num': result['success_num'], 'total': result['total']})
        except TypeError:
            pass
        return HttpResponseRedirect(change_url)

    def group_send_push(self, request, message_id):
        change_url = reverse("admin:push_message_change", args=(message_id,))
        result = send_push_by_message_template(message_id=message_id, receiver='group')
        try:
            if 'error' in result:
                messages.error(request, result['error'])
            elif 'total' in result and 'success_num' in result:
                info_message = _('%(success_num)d of %(total)d push notifications were sent successfully')
                messages.info(request, info_message % {'success_num': result['success_num'], 'total': result['total']})
        except TypeError:
            pass
        return HttpResponseRedirect(change_url)


# @admin.register(MessageClient)
# class MessageClientAdmin(admin.ModelAdmin):
#     list_display = ['message', 'client', 'created_at']
#     readonly_fields = ['created_at']


@admin.register(ServiceQualityAnswers)
class ServiceQualityAnswersAdmin(admin.ModelAdmin):
    list_display = ['location', 'client', 'id_clean', 'id_products_quality', 'id_service_quality', 'created_at']

