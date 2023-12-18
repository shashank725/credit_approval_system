from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval_system.settings_dev')

# create a Celery instance and configure it with the Django settings.
celery_app = Celery('credit_approval_system')

# Update timezone
celery_app.conf.enable_utc = False
celery_app.conf.update(timezone = 'Asia/Kolkata')

# Load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# celery_app.config_from_object(settings, namespace='CELERY')   # Not using line 4

# Auto-discover tasks in all installed apps
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
