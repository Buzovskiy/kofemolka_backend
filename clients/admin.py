from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.translation import gettext_lazy as _
from .models import Clients, Comment, Proposal
from .exchange import import_clients


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'firstname', 'lastname')
    list_display_links = ('client_id', 'firstname')
    readonly_fields = ('client_id',)
    inlines = [CommentInline]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update-clients-from-api/', self.update_clients_from_api),
        ]
        return my_urls + urls

    def update_clients_from_api(self, request):
        try:
            objects_added = 0
            res = import_clients()
            if 'objects_created' in res:
                objects_added = res['objects_created']
            messages.success(request, f'{objects_added} {_("objects added")}')
        except:
            messages.error(request, 'e')
        return HttpResponseRedirect("../")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'rating', 'response', 'approved', 'client', 'location')
    list_display_links = ('id', 'comment')


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'proposal')
