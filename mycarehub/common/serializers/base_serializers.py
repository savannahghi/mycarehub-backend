"""Base serializers used in the project."""
import logging

from .mixins import AuditFieldsMixin

LOGGER = logging.getLogger(__name__)


class BaseSerializer(AuditFieldsMixin):
    """Base class intended for inheritance by 'regular' app serializers."""

    class Meta:
        datatables_always_serialize = ("id",)
