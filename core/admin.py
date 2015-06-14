from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db.models.query_utils import Q
from core.models import Log, Entry

__author__ = 'alexandreferreira'

class EntryAdmin(ModelAdmin):

    def get_queryset(self, request):
        qs = super(EntryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(Q(deleted=True) | Q(deleted=False))
        else:
            return qs

admin.site.register(Entry)
admin.site.register(Log)