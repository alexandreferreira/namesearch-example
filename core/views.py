from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView
from core.forms import EntryForm
from core.models import Entry, Log

__author__ = 'alexandreferreira'

class Home(TemplateView):
    template_name = "home/home.html"

class SearchEntry(TemplateView):
    template_name = "search/search_entry.html"

class SearchLog(TemplateView):
    template_name = "search/search_log.html"

class ListLog(ListView):
    model = Log
    paginate_by = 500
    template_name = "entry/log_list.html"
    queryset = Log.objects.all()
    context_object_name = 'logs'

class ListEntries(ListView):
    model = Entry
    paginate_by = 500
    template_name = "entry/entry_list.html"
    queryset = Entry.objects.all()
    context_object_name = 'entries'

class UpdateEntry(UpdateView):
    model = Entry
    queryset = Entry.objects.all()
    form_class = EntryForm
    template_name = "entry/entry_form.html"

    def get_success_url(self):
        return reverse_lazy('entry_list')


class CreateEntry(CreateView):
    model = Entry
    queryset = Entry.objects.all()
    form_class = EntryForm
    template_name = "entry/entry_form.html"

    def get_success_url(self):
        return reverse_lazy('entry_list')


class DeleteEntry(DeleteView):
    model = Entry
    queryset = Entry.objects.all()
    template_name = "entry/entry_delete.html"

    def get_success_url(self):
        return reverse_lazy('entry_list')