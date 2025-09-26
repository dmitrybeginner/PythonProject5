import os

from celery import Celery

# Устанавливаем модуль настроек Django по умолчанию для программы 'celery'.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Использование здесь строки означает, что воркеру не нужно сериализовать
# объект конфигурации для дочерних процессов.
# - пространство имен 'CELERY' означает, что все ключи конфигурации, связанные с Celery,
#   должны иметь префикс `CELERY_`.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Загружаем модули задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks()
