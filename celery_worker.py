from celery import Celery
from celery.schedules import crontab
import os

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
celery_app.conf.timezone = 'Asia/Kolkata'


celery_app.conf.beat_schedule = {
    "reset-daily": {
        "task": "tasks.reset_inventory_data",
        "schedule": crontab(hour=22, minute=40),  # Daily at 9 PM IST
        "args": ("697bb2385a71768f00baf088", 100)  # Example args
    }
}