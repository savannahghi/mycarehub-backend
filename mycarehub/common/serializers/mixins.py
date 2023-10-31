"""Shared serializer mixins."""
import logging

from rest_framework import exceptions, serializers

from mycarehub.common.models import Organisation

LOGGER = logging.getLogger(__name__)


def get_organisation(request, initial_data=None):
    """Determine the organisation based on the user and supplied data."""

    user = request.user
    organisation = (
        initial_data.get("organisation")
        if isinstance(initial_data, dict)
        else request.data.get("organisation")
    )

    if organisation:
        try:
            org = Organisation.objects.get(id=organisation)
        except Organisation.DoesNotExist as no_org:
            error = {"organisation": "Ensure the organisation provided exists."}
            raise exceptions.ValidationError(error) from no_org
        return org
    else:
        return user.organisation


class AuditFieldsMixin(serializers.ModelSerializer):
    """Mixin for organisation, created, updated, created_by and updated_by."""

    def __init__(self, *args, **kwargs):
        """Initialize the mixin by marking the fields it manages as read-only."""

        super().__init__(*args, **kwargs)
        audit_fields = "created", "created_by", "updated", "updated_by", "organisation"
        for field_name in audit_fields:
            if field_name in self.fields:  # pragma: nobranch
                self.fields[field_name].read_only = True

    def populate_audit_fields(self, data, is_create):
        request = self.context["request"]
        user = request.user
        data["updated_by"] = user.pk
        if is_create:
            data["created_by"] = user.pk

            # Do not do this for an Organisation serializer
            # or a model that does not have an organisation attribute
            has_organisation = getattr(self.Meta.model, "organisation", None) is not None
            if self.Meta.model != Organisation and has_organisation:  # pragma: nobranch
                # If an 'organisation' is not explicitly passed in,
                # use the logged in user's organisation, if the request if
                # for creation only
                data["organisation"] = get_organisation(request, self.initial_data)
        return data

    def create(self, validated_data):
        """Ensure that ids are not supplied when creating new instances."""
        self.populate_audit_fields(validated_data, True)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Ensure that audit fields are set when updating."""
        self.populate_audit_fields(validated_data, False)
        return super().update(instance, validated_data)
