from haystack.query import SearchQuerySet
from rest_framework.generics import ListAPIView
from core.models import Entry, Log
from core.serialize import EntrySerializer, LogSerializer

__author__ = 'alexandreferreira'


class SearchEntryAPIView(ListAPIView):

    serializer_class = EntrySerializer

    def get_queryset(self):
        if self.request.query_params.get('q'):
            search = self.request.query_params['q']
            return SearchQuerySet().filter(content=search).models(*[Entry])
            # return Entry.objects.search_text(search)
        else:
            return []


class SearchLogAPIView(ListAPIView):

    serializer_class = LogSerializer

    def get_queryset(self):
        if self.request.query_params.get('q'):
            search = self.request.query_params['q']
            return SearchQuerySet().filter(content=search).models(*[Log])
        else:
            return []