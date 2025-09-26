"""
ASGI конфигурация для проекта core.

Этот файл предоставляет ASGI-совместимое веб-приложение как переменную
уровня модуля с именем ``application``.

Для получения дополнительной информации по этому файлу см.
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_asgi_application()
