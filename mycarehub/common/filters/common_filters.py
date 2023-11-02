import django_filters
from rest_framework import filters

from ..models import Facility, UserFacilityAllotment


class FacilityFilter(django_filters.FilterSet):
    """Filter facilities."""

    search = filters.SearchFilter()

    class Meta:
        """Set up filter options."""

        model = Facility
        fields = "__all__"


class UserFacilityAllotmentFilter(django_filters.FilterSet):
    search = filters.SearchFilter()

    class Meta:
        model = UserFacilityAllotment
        fields = ("user",)
