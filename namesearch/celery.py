from __future__ import absolute_import
from celery import Celery
import os
__author__ = 'alexandreferreira'

if os.getenv('host') == 'PROD':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'namesearch.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'namesearch.settings')

from django.conf import settings

app = Celery('namesearch')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)