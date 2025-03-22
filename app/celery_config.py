import os
from celery import Celery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Redis URL from .env
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

# Initialize Celery
celery_app = Celery("bulk_image_processor", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Celery Configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks(['app.tasks'])