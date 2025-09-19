from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()
        logger.info(f'Пользователь {user.email} был деактивирован из-за неактивности.')