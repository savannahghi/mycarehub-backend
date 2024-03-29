import logging
import uuid
from collections import defaultdict
from typing import List, Tuple, TypeVar

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.db.models.base import ModelBase
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from mycarehub.utils.general_utils import default_organisation

from .organisation_models import Organisation
from .utils import unique_list

LOGGER = logging.getLogger(__file__)
T_OA = TypeVar("T_OA", bound="OwnerlessAbstractBase", covariant=True)


# =============================================================================
# QUERYSETS
# =============================================================================


class OwnerlessAbstractBaseQuerySet(models.QuerySet[T_OA]):  # noqa
    """Base queryset for all models not linked to an organisation."""

    def active(self):
        """Return all records marked as active."""
        return self.filter(active=True)

    def non_active(self):
        """Return all records marked as non active."""
        return self.filter(active=False)


class AbstractBaseQuerySet(OwnerlessAbstractBaseQuerySet[T_OA]):  # noqa
    """Base queryset for all models linked to an organisation."""

    ...


# =============================================================================
# MANAGERS
# =============================================================================


class OwnerlessAbstractBaseManager(models.Manager[T_OA]):  # noqa
    """Base manager for all models not linked to an organisation."""

    use_for_related_fields = True
    use_in_migrations = True

    def active(self):
        """Return all the records marked as active."""
        return self.get_queryset().active()

    def get_queryset(self):
        return OwnerlessAbstractBaseQuerySet(self.model, using=self.db)  # pragma: nocover

    def non_active(self):
        """Return all the records marked as non-active."""
        return self.get_queryset().non_active()


class AbstractBaseManager(OwnerlessAbstractBaseManager[T_OA]):  # noqa
    """Base queryset for all models linked to an organisation."""

    use_for_related_fields = True
    use_in_migrations = True

    def get_queryset(self):
        return AbstractBaseQuerySet(self.model, using=self.db)


# =============================================================================
# META CLASSES
# =============================================================================


class ValidationMetaclass(ModelBase):
    """Ensures model_validators defined in parent are retained in child models.

    For example:

        class Parent(models.Model):
            model_validators = ["a"]

        class Child(models.Model(Parent):
            model_validators = ["b"]

        assert Child().model_validators == ["a", "b"]  # True
    """

    def __new__(cls, name, bases, attrs):
        """Customize the model metaclass - add support for model_validators."""
        _model_validators = []
        for each in bases:
            if hasattr(each, "model_validators"):
                _model_validators.extend(each.model_validators)
        _model_validators.extend(attrs.get("model_validators", []))
        attrs["model_validators"] = _model_validators
        return super(ValidationMetaclass, cls).__new__(cls, name, bases, attrs)


# =============================================================================
# BASE CLASSES
# =============================================================================


class OwnerlessAbstractBase(models.Model, metaclass=ValidationMetaclass):
    """Base class for models that are not linked to an organisation."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    created_by = models.UUIDField(null=True, blank=True)
    updated = models.DateTimeField(default=timezone.now)
    updated_by = models.UUIDField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = OwnerlessAbstractBaseManager()

    model_validators = ["validate_updated_date_greater_than_created"]

    def _raise_errors(self, errors):
        if errors:
            raise ValidationError(errors)

    def validate_updated_date_greater_than_created(self):
        """Ensure that updated is always after created."""
        if self.updated and self.created and self.updated.date() < self.created.date():
            # using dates to avoid a lot of fuss about milliseconds etc
            raise ValidationError("The updated date cannot be less than the created date")

    def preserve_created_and_created_by(self):
        """Ensure that in created and created_by fields are not overwritten."""
        try:
            original = self.__class__.objects.get(pk=self.pk)
            self.created = original.created
            self.created_by = original.created_by
        except self.__class__.DoesNotExist:
            LOGGER.debug(
                "preserve_created_and_created_by "
                "Could not find an instance of {} with pk {} hence treating "
                "this as a new record.".format(self.__class__, self.pk)
            )

    def run_model_validators(self):
        """Ensure that all model validators run."""
        validators = getattr(self, "model_validators", [])
        self.run_validators(validators)

    def run_validators(self, validators):
        """Run declared model validators."""
        errors = defaultdict(list)

        for validator in unique_list(validators):
            try:
                getattr(self, validator)()
            except ValidationError as e:
                if hasattr(e, "error_dict"):
                    for key, messages in e.message_dict.items():
                        # messages is ValidationError instances list
                        errors[key].extend(messages)
                else:
                    errors["__all__"].extend(e.messages)

        self._raise_errors(errors)

    def clean(self):
        """Run validators declared under model_validators."""
        self.run_model_validators()
        super().clean()

    def save(self, *args, **kwargs):
        """Handle audit fields correctly when saving."""
        self.updated = timezone.now() if self.updated is None else self.updated
        self.preserve_created_and_created_by()
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        """Define a sensible default ordering."""

        abstract = True
        ordering: Tuple[str, ...] = ("-updated", "-created")


class AbstractBase(OwnerlessAbstractBase):
    """Base class for most models in the application."""

    # this differs from Ownerless Abstract Base only in adding the organisation
    # field
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
        default=default_organisation,
    )

    objects = AbstractBaseManager()

    organisation_verify: List[str] = []
    model_validators = [
        "validate_organisation",
        "validate_updated_date_greater_than_created",
    ]

    @property
    def owner(self):
        """Return the record's owner."""
        return self.organisation.org_code

    def validate_organisation(self):
        """Verify that orgs in FKs are consistent with those being created."""
        error_msg = (
            "The organisation provided is not consistent with that of organisation fields in "
            "related resources"
        )
        if self.organisation_verify:
            for field in self.organisation_verify:  # pragma: nocover
                value = getattr(self, field)
                if value and str(self.organisation.id) != str(value.organisation.id):
                    LOGGER.error(f"{field} has an inconsistent org")
                    raise ValidationError({"organisation": _(error_msg)})

    class Meta(OwnerlessAbstractBase.Meta):
        """Define a sensible default ordering."""

        abstract = True
