from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Course, Lesson
from .tasks import send_course_update_email

@receiver(pre_save, sender=Course)
def course_update_signal(sender, instance, **kwargs):
    if instance.pk:  # Проверяем, что это обновление, а не создание нового объекта
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if timezone.now() - old_instance.last_updated > timedelta(hours=4):
                send_course_update_email.delay(instance.id)
                instance.last_updated = timezone.now()
        except sender.DoesNotExist:
            pass # Не должно происходить при обновлении

@receiver(pre_save, sender=Lesson)
def lesson_update_signal(sender, instance, **kwargs):
    if instance.pk:
        course = instance.course
        if timezone.now() - course.last_updated > timedelta(hours=4):
            send_course_update_email.delay(course.id)
            course.last_updated = timezone.now()
            course.save()