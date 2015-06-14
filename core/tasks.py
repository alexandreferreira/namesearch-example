from celery.app import shared_task
from core.models import Log
from core.utils import import_random_names
__author__ = 'alexandreferreira'


@shared_task
def register_log_entry_create(number, text):
    Log.objects.register_create_entry(number, text)


@shared_task
def register_log_entry_update(number, text):
    Log.objects.register_edit_entry(number, text)


@shared_task
def register_log_entry_viewed(number, text):
    Log.objects.register_view_entry(number, text)


@shared_task
def register_log_entry_deleted(number, text):
    Log.objects.register_delete_entry(number, text)


@shared_task
def register_log_entries_created(entries):
    for entry in entries:
        register_log_entry_create.delay(entry[0], entry[1])

@shared_task
def import_names():
    return import_random_names()


@shared_task
def update_index():
    from haystack.management.commands import update_index
    update_index.Command().handle()
