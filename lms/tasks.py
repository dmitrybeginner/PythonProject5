from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from lms.models import Course
from users.models import Subscription
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)
        recipient_emails = [sub.user.email for sub in subscriptions]

        if not recipient_emails:
            return

        send_mail(
            subject=f'Обновление курса: {course.name}',
            message=f'Курс "{course.name}", на который вы подписаны, был обновлен.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_emails,
            fail_silently=False,
        )
        logger.info(f"Отправлено письмо об обновлении курса {course.id} для {len(recipient_emails)} подписчиков.")

    except Course.DoesNotExist:
        # Обрабатываем случай, когда курс может быть удален до выполнения задачи
        pass