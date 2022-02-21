from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommunityConfig(AppConfig):
    name = "mycarehub.communities"
    verbose_name = _("Communities")
