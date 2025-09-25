from datetime import timedelta

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from users.models import User

logger = get_task_logger(__name__)


@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()
        logger.info(f"Пользователь {user.email} был деактивирован из-за неактивности.")
