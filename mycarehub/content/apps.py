from django.apps import AppConfig
from django.conf import settings
from willow.registry import registry


class ContentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mycarehub.content"

    def ready(self):
        if settings.SETTINGS_MODULE != "config.settings.test":  # pragma: nocover
            from . import signals  # noqa F401
        import rustface.willow  # noqa

        registry.register_plugin(rustface.willow)
