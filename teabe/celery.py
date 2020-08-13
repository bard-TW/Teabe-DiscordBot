import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teabe.settings')
app = Celery('teabe')
app.conf.enable_utc = False
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()