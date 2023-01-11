import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import (
    PROTECT,
    BooleanField,
    CharField,
    ForeignKey,
    JSONField,
    TextChoices,
    TextField,
    UUIDField,
)
from django.db.models.base import Model
from django.db.models.fields import DateField, DateTimeField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from mycarehub.utils.general_utils import default_organisation, default_program


class UserTypes(TextChoices):
    CLIENT = "CLIENT", _("Client")
    STAFF = "STAFF", _("Staff")


class GenderChoices(TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    OTHER = "OTHER", _("Other")


class User(AbstractUser):
    """Default user model."""

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    #: First and last name do not cover name patterns around the globe
    # this should be used as the display name
    name = CharField(_("Name of User"), blank=True, max_length=255)
    middle_name = TextField(blank=True)
    gender = CharField(choices=GenderChoices.choices, max_length=16, null=True, blank=True)
    date_of_birth = DateField(null=True, blank=True)
    user_type = CharField(choices=UserTypes.choices, max_length=32, null=True, blank=True)
    organisation = ForeignKey(
        "common.Organisation",
        on_delete=PROTECT,
        default=default_organisation,
    )
    program = ForeignKey(
        "common.Program", on_delete=PROTECT, default=default_program, null=True, blank=True
    )

    @property
    def permissions(self):
        perms = set(
            [
                f"{perm.content_type.app_label}.{perm.codename}"
                for perm in self.user_permissions.all()
            ]
        )
        groups = self.groups.all()
        for group in groups:
            group_perms = set(
                [
                    f"{perm.content_type.app_label}.{perm.codename}"
                    for perm in group.permissions.all()
                ]
            )
            perms = perms | group_perms
        return ",\n".join(list(perms))

    @property
    def gps(self):
        groups = [gp.name for gp in self.groups.all()]
        return ",".join(groups) or "-"

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        username = self.get_username()
        return f"{self.name} ({username})" if self.name else username

    class Meta(AbstractUser.Meta):
        permissions = [
            ("can_view_dashboard", "Can View Dashboard"),
            ("can_view_about", "Can View About Page"),
            ("can_export_data", "Can Export Data"),
            ("can_import_data", "Can Import Data"),
            ("system_administration", "System Administration"),
            ("content_management", "Content Management"),
            ("client_management", "Client Management"),
        ]


class Metric(Model):
    class MetricType(TextChoices):
        ENGAGEMENT = "ENGAGEMENT", _("Engagement Metrics")
        CONTENT = "CONTENT", _("Content Metrics")
        SYSTEM = "SYSTEM", _("System Metrics")

    timestamp = DateTimeField(default=timezone.now)
    payload = JSONField()
    user = ForeignKey(User, on_delete=PROTECT)
    metric_type = CharField(choices=MetricType.choices, max_length=32)
    active = BooleanField(default=True)
    created = DateTimeField(default=timezone.now)
    created_by = UUIDField(null=True, blank=True)
    updated = DateTimeField(default=timezone.now)
    updated_by = UUIDField(null=True, blank=True)
    deleted_at = DateTimeField(null=True, blank=True)
