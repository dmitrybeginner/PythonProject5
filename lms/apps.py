from django.apps import AppConfig


class LmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lms"

    def ready(self):
        print("--- LMS APP IS READY, SIGNALS IMPORTED ---")
        import lms.signals
