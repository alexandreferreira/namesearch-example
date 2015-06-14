from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from core.api import SearchEntryAPIView, SearchLogAPIView
from core.views import Home, ListEntries, UpdateEntry, CreateEntry, DeleteEntry, SearchEntry, SearchLog, ListLog

admin.autodiscover()

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    url(r'^entry/$', ListEntries.as_view(), name='entry_list'),
    url(r'^entry/create/$', CreateEntry.as_view(), name='entry_create'),
    url(r'^entry/edit/(?P<pk>\d+)/$', UpdateEntry.as_view(), name='entry_update'),
    url(r'^entry/delete/(?P<pk>\d+)/$', DeleteEntry.as_view(), name='entry_delete'),
    url(r'^entry/search/$', SearchEntry.as_view(), name='entry_search'),

    url(r'^log/search/$', SearchLog.as_view(), name='log_search'),
    url(r'^log/$', ListLog.as_view(), name='log_list'),

    url(r'^api/entry/search/$', SearchEntryAPIView.as_view(), name='entry_search_api'),
    url(r'^api/log/search/$', SearchLogAPIView.as_view(), name='log_search_api'),

    url(r'^$', Home.as_view(), name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)