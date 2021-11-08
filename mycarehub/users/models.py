import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import PROTECT, BooleanField, CharField, ForeignKey, TextField, UUIDField
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.db.utils import ProgrammingError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from mycarehub.common.models.base_models import AbstractBase
from mycarehub.common.models.common_models import Facility

DEFAULT_ORG_CODE = 1


def default_organisation():
    try:
        from mycarehub.common.models import Organisation  # intentional late import

        org, _ = Organisation.objects.get_or_create(
            code=DEFAULT_ORG_CODE,
            id=settings.DEFAULT_ORG_ID,
            defaults={
                "organisation_name": settings.ORGANISATION_NAME,
                "email_address": settings.ORGANISATION_EMAIL,
                "phone_number": settings.ORGANISATION_PHONE,
            },
        )
        return org.pk
    except (ProgrammingError, Exception):  # pragma: nocover
        # this will occur during initial migrations on a clean db
        return settings.DEFAULT_ORG_ID


class User(AbstractUser):
    """Default user model."""

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    #: First and last name do not cover name patterns around the globe
    # this should be used as the display name
    name = CharField(_("Name of User"), blank=True, max_length=255)

    first_name = TextField(blank=True)
    last_name = TextField(blank=True)
    middle_name = TextField(blank=True)
    username = TextField(blank=True)  # @handle

    # TODO: UserType string // e.g client, health care worker, choices
    # TODO: Gender string // genders; keep it simple
    # TODO: active...make a custom manager (objects) that ignores inactive users
    # TODO: PushTokens []string
    # TODO: LastSuccessfulLogin *time.Time
    # TODO: LastFailedLogin *time.Time
    # TODO: FailedLoginCount int
    # TODO: NextAllowedLogin *time.Time
    # TODO: FK to terms of service that were accepted
    # TODO: computed terms accepted field

    is_approved = BooleanField(
        default=False,
        help_text="When true, the user is able to log in to the main website (and vice versa)",
    )
    approval_notified = BooleanField(
        default=False,
        help_text="When true, the user has been notified that their account is approved",
    )
    phone = PhoneNumberField(null=True, blank=True)
    organisation = ForeignKey(
        "common.Organisation",
        on_delete=PROTECT,
        default=default_organisation,
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
            # TODO Add roles here, piggy back on Django RBAC
        ]


# TODO Sensible behavior for first name, last name and name fields


class UserPIN(AbstractBase):
    user = ForeignKey(User)
    hashed_pin = TextField()
    valid_from = DateTimeField(auto_now_add=True)
    valid_to = DateTimeField(auto_now_add=True)
    # TODO: flavour choices...Pro or Consumer
    # TODO: computed is_valid property
    # TODO: composite index, user and flavour


# TODO: API: invite, for a specific flavour
#   send deep link via SMS..custom per user
#   generate random PIN and save it, set it to expire at once
# TODO: API: set PIN/change PIN
#   audit all PINs...save each version, inactivate previous ones
#   Consult CLIENT_PIN_VALIDITY_DAYS and PRO_PIN_VALIDITY DAYS env/setting to set expiry
#   use Django password hashing algorithm
#   ensure that old PINs are not reused
#   Each time a PIN is set, recalculate valid to / valid from
# TODO: API: login: Login(userID string, pin string, flavour string)
#   verify PIN
#   if not active, can't login
#   if a login is not allowed yet, treat as a failure
#   if future expiry...allow login
#   if past...require change...code
#   only users who have accepted terms can log in
#   if all checks pass, return OAuth access token and refresh token
#   only allow active, not forgotten users to log in
#   For successful logins, reset last failed login and failed login count; set last
# successful login
#   For failed logins: increment failed login count, update last failed login timestamp,
# set next allowed login timestamp
#       - calculate next allowed login as base (from setting, default 3) ^ failed_login_count
#       - record next allowed login
# TODO: API: forget...Forget(userID string, pin string, flavour string) (bool, error)
# TODO: API: request data export...RequestDataExport(userID string, pin string,
# flavour string) (bool, error)
# TODO: API: ResetPIN(userID string, flavour string) (bool, error), for admins to
# generate a new PIN
# TODO: API: VerifyPIN(userID string, flavour string, pin string), to check PIN for
# sensitive content
# TODO: API: GetAnonymizedUserIdentifier(userID string, flavour string) (string, error)
# TODO: API: patch, consider if the items below should be implemented directly
# TODO: API: AddPushtoken(userID string, flavour string) (bool, error)
# TODO: API: RemovePushToken(userID string, flavour string) (bool, error)


class StaffProfile(AbstractBase):
    user = OneToOneField(User, on_delete=PROTECT)
    staff_number = TextField()
    default_facility = ForeignKey(Facility, on_delete=PROTECT)
    facilities = ManyToManyField(Facility, related_name="staff_facilities")


# TODO API to query a staff user's roles
# TODO API to update default facility
# TODO CRUD, admin for staff profiles


class Action(AbstractBase):
    """
    type Action struct {
        ID string

        Name    string
        Payload map[string]string
        Icon    string // TODO link
    }
    """

    # TODO Implement action model
    pass


class Notification(AbstractBase):
    """
    type Notification struct {
        ID string

        Title            string
        Body             string   // TODO: might be **formatted** e.g MD
        Link             string   // TODO: not all notifications need this but for some
        (e.g surveys) this is the main thing
        Icon             string   // TODO: link
        Badge            []string // TODO: e.g to mark missed appointments
        Status           string   // TODO: enum e.g resolved, pending
        NotificationType string   // TODO: enum e.g appointment, survey, article; use to
        create "blind" display
        Channels         []string // TODO: enums e.g PUSH, SMS
        Timestamp        time.Time
        Actions          []*Action
        Flavour          string // TODO enum
    }
    """

    # TODO Implement notification model
    pass


# TODO: API, send single notification
# TODO: API, send survey notification
# TODO: API, send group notifications
