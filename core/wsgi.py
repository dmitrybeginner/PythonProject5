"""
WSGI конфигурация для проекта core.

Этот файл предоставляет WSGI-совместимое веб-приложение как переменную
уровня модуля с именем ``application``.

Для получения дополнительной информации по этому файлу см.
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()
