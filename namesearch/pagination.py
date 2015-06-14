from collections import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response

__author__ = 'alexandreferreira'


class DetailPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_page_number()),
            ('has_next', self.page.has_next()),
            ('previous', self.get_previous_page_number()),
            ('has_previous', self.page.has_previous()),
            ('current', self.page.number),
            ('results', data)
        ]))

    def get_next_page_number(self):
        if not self.page.has_next():
            return self.page.number
        return self.page.next_page_number()

    def get_previous_page_number(self):
        if not self.page.has_previous():
            return 1
        return self.page.previous_page_number()