import django_filters
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.filters import BaseFilterBackend
from wagtail.admin.filters import WagtailFilterSet

from mycarehub.clients.models import Client
from mycarehub.common.filters.base_filters import CommonFieldsFilterset
from mycarehub.common.models import ContentSequence
from mycarehub.content.models import ContentItem
from mycarehub.content.models.fafanuka import FafanukaContentItem

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


class ContentSequenceFilter(BaseFilterBackend):
    """
    Implements a content sequence filter. The sequence determines how/when content is served
    i.e based on the time a user joined which allows gradual delivery of content to a user.

    This filter accepts a client_id.
    """

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        client_id = query_params.get("client_id", "")

        if client_id and queryset.model is ContentItem:
            try:
                client = Client.objects.get(id=client_id)
            except ObjectDoesNotExist:
                return queryset

            program = client.program

            if program.content_sequence == ContentSequence.GRADUAL:
                # How long a client has been active since creation/enrollment
                today = timezone.now()
                client_active_delta = today - client.enrollment_date

                # Determine the content to show i.e up to which date
                effective_date = program.start_date + client_active_delta

                return queryset.filter(date__lte=effective_date)

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


class FafanukaFilterSet(BaseFilterBackend):
    """
    Filter fafanuka content backend.

    Fafanuka filters by:
        1. Category (offer)
        2. Language - the language the content should be returned in
        3. End (Last content sequence) - to get the next content that should be returned
    """

    def filter_queryset(self, request, queryset, view):
        """Filter queryset by category, language and last sequence."""

        if queryset.model is FafanukaContentItem:
            query_params = request.query_params
            default_filters = {
                "organisation": request.user.organisation,
                "program": request.user.program,
                "live": True,  # TODO: Remember to change this to happen only after publishing
            }

            initial_content = query_params.get("initial_content", "")
            if initial_content:
                filters = {
                    "subgroup": FafanukaContentItem.SubGroup.DIABETES_GENERAL_INFORMATION.value,
                    "sequence_number": 1,
                    "offer": FafanukaContentItem.OfferType.GENERAL_TIPS,
                }
                filters.update(default_filters)
                return queryset.filter(**filters)

            # Check sequence - based on some previous sequence
            offer = query_params.get("offer_code", "")
            default_filters.update(
                {
                    "offer__in": [offer, FafanukaContentItem.OfferType.GENERAL_TIPS.value],
                }
            )
            current_sequence_number = query_params.get(
                "current_sequence_number", ""
            )  # TODO: Validate not 0
            current_subgroup = query_params.get("current_subgroup", "")
            next_sequence_number = (
                int(current_sequence_number) + 1
            )  # Programatically get the next one (don't assume next is always +1)

            subgroup_filters = {"subgroup": current_subgroup}  # TODO Handle None([])
            subgroup_filters.update(default_filters)
            current_subgroup_last_sequence_number = (
                FafanukaContentItem.objects.filter(**subgroup_filters)
                .order_by("sequence_number")
                .last()
                .sequence_number
            )
            if next_sequence_number <= current_subgroup_last_sequence_number:
                subgroup_filters.update({"sequence_number": next_sequence_number})
                return queryset.filter(**subgroup_filters)

            # Other subgroups outside the current one
            content = FafanukaContentItem.objects.filter(**default_filters).order_by("subgroup")
            last_subgroup = content.last().subgroup
            next_subgroup = int(current_subgroup) + 1
            if next_subgroup <= last_subgroup:  # We are still within content pool so we can send
                default_filters.update(
                    {
                        "subgroup": next_subgroup,
                    }
                )
                return queryset.filter(**default_filters).order_by("sequence_number")

            return FafanukaContentItem.objects.none()

        return queryset
