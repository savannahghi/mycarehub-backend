from rest_framework import filters

from mycarehub.content.models import (
    ContentBookmark,
    ContentItemCategory,
    ContentLike,
    ContentShare,
    ContentView,
)


class OrganisationFilterBackend(filters.BaseFilterBackend):
    """Users are only allowed to view records in their organisation."""

    def filter_queryset(self, request, queryset, view):
        """Filter all records that have an organisation field by user org."""
        if queryset.model in [
            ContentItemCategory,
            ContentBookmark,
            ContentLike,
            ContentShare,
            ContentView,
        ]:
            return queryset
        return queryset.filter(organisation=request.user.organisation)
