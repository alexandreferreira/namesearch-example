from django.utils import timezone
from core.models import Entry, Log

__author__ = 'alexandreferreira'

from haystack import indexes

class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, model_attr='text')
    number = indexes.IntegerField(model_attr='number')
    updated = indexes.DateTimeField(model_attr='updated')

    def get_model(self):
        return Entry

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def get_updated_field(self):
        return "updated"

class LogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, model_attr='old_text')
    text_actual = indexes.NgramField(model_attr='entry__text')
    entry = indexes.IntegerField(model_attr='entry_id')
    log_type = indexes.CharField(model_attr='log_type')
    updated = indexes.DateTimeField(model_attr='updated')

    def get_model(self):
        return Log

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all().prefetch_related("entry")

    def get_updated_field(self):
        return "updated"
