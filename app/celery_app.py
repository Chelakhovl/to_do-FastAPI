import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=os.getenv("CELERY_RESULT_BACKEND", REDIS_URL),
)

celery_app.conf.update(
    task_routes={"app.tasks.fetch_and_save_users": {"queue": "users"}},
    timezone=os.getenv("TIMEZONE", "Europe/Kyiv"),
    beat_schedule={
        "fetch-users-hourly": {
            "task": "app.tasks.fetch_and_save_users",
            "schedule": 60 * 60,
        }
    },
)
