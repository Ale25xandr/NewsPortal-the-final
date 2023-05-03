import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'week_post': {
        'task': 'NewsPortal.tasks.week_post',
        'schedule': crontab(minute=0, hour=8, day_of_week='mon'),
        'args': ()
    },
}