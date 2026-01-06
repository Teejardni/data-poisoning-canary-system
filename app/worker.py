from celery import Celery
from app.core.settings import settings

celery_worker = Celery(settings.app_name, broker=f'{settings.redis_endpoint}')


@celery_worker.task
def health_check():
    from datetime import datetime
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
