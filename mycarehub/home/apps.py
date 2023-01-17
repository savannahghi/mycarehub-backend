from django.apps import AppConfig
from django.conf import settings


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mycarehub.home"

    def ready(self):
        if settings.SETTINGS_MODULE != "config.settings.test":  # pragma: nocover
            from . import signals  # noqa F401
