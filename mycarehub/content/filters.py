import django_filters
from django.db.models import Count, Q
from rest_framework.filters import BaseFilterBackend
from wagtail.admin.filters import WagtailFilterSet

from mycarehub.common.filters.base_filters import CommonFieldsFilterset
from mycarehub.content.models import ContentItem

from .models import (
    Author,
    ContentBookmark,
    ContentItemCategory,
    ContentLike,
    ContentShare,
    ContentView,
)


class TagFilter(BaseFilterBackend):
    """
    Implements the ?tag filter which returns only pages that match a tag.

    This filter accepts a single tag.
    """

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        tag = query_params.get("tag", "")

        if tag and queryset.model is ContentItem:
            queryset = queryset.filter(Q(tags__name=tag) | Q(tags__slug=tag))

        return queryset


class CategoryFilter(BaseFilterBackend):
    """
    Implements the ?category filter which returns only pages that match a
    category ID.

    This filter accepts a single category ID.
    When no filter is passed, the category ID 1
    which is reserved for `welcome` content type is excluded.
    """

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        category_id = query_params.get("category", "")
        category_name = query_params.get("category_name", "")

        if category_name and queryset.model is ContentItem:
            queryset = queryset.filter(Q(categories__name=category_name))
        if category_id and queryset.model is ContentItem:
            queryset = queryset.filter(Q(categories__id=category_id))

        return queryset


class ClientFilter(BaseFilterBackend):
    """
    Implements the client_id filter which returns only pages that a specific client can view

    This filter accepts a client_id. Client properties are then used to filter content that is
    "personalised" to the specific client. Currently includes:

    - the program they belong to
    """

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        client_id = query_params.get("client_id", "")

        if client_id and queryset.model is ContentItem:
            queryset = queryset.filter(Q(program__clients=client_id))

        return queryset


class FacilityFilter(BaseFilterBackend):
    """
    Implements the facility_id filter which only returns pages from a specific facility
    """

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        facility_id = query_params.get("facility_id", "")

        if facility_id and queryset.model is ContentItem:
            queryset = queryset.filter(Q(facilities=facility_id))

        return queryset


class ContentItemCategoryFilter(CommonFieldsFilterset):
    def category_has_content(self, queryset, field, value):
        """
        Ensures the category has content in it
        """
        return queryset.annotate(content_count=Count("contentitem")).filter(content_count__gte=1)

    has_content = django_filters.BooleanFilter(method="category_has_content")
    program_id = django_filters.UUIDFilter(field_name="programs", lookup_expr="exact")

    class Meta:
        model = ContentItemCategory
        fields = "__all__"


class ContentViewFilter(CommonFieldsFilterset):
    class Meta:
        model = ContentView
        fields = "__all__"


class ContentShareFilter(CommonFieldsFilterset):
    class Meta:
        model = ContentShare
        fields = "__all__"


class ContentLikeFilter(CommonFieldsFilterset):
    class Meta:
        model = ContentLike
        fields = "__all__"


class ContentBookmarkFilter(CommonFieldsFilterset):
    class Meta:
        model = ContentBookmark
        fields = "__all__"


class ContentItemCategoryFilterSet(WagtailFilterSet):
    def filter_queryset(self, *args, **kwargs):
        return self.queryset.filter(organisation=self.request.user.organisation)

    class Meta:
        model = ContentItemCategory
        fields = ["name"]


class AuthorFilterSet(WagtailFilterSet):
    def filter_queryset(self, *args, **kwargs):
        return self.queryset.filter(organisation=self.request.user.organisation)

    class Meta:
        model = Author
        fields = ["name"]
