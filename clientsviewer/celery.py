import os

from celery import Celery 

app=Celery('clientsviewer')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clientsviewer.settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
