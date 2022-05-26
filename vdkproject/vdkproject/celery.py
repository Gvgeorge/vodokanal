import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vdkproject.settings')

app = Celery('vdkproject')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update_order_table_60s': {
        'task': 'vdkapp.tasks.update_order_table',
        'schedule': 60.0
    }
}
app.autodiscover_tasks()
