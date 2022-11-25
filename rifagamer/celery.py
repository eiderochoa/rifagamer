# Django settings
from __future__ import absolute_import
import os, sys
from django.conf import settings
# Celery app
from celery import Celery

sys.path.append(os.path.abspath('rifagamer'))
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rifagamer.settings')

app = Celery('rifagamer', broker='redis://localhost')

# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()