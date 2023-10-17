from django.urls import path
from wagtail.api.v2.filters import (
    AncestorOfFilter,
    ChildOfFilter,
    DescendantOfFilter,
    FieldsFilter,
    LocaleFilter,
    OrderingFilter,
    SearchFilter,
    TranslationOfFilter,
)
from wagtail.api.v2.views import PagesAPIViewSet

from mycarehub.common.views.base_views import BaseView
from mycarehub.content.filters import (
    CategoryFilter,
    ClientFilter,
    ContentFilter,
    ContentItemCategoryFilter,
    ContentSequenceFilter,
    FacilityFilter,
    SMSContentItemFilterSet,
    TagFilter,
)
from mycarehub.content.models import ContentItemCategory
from mycarehub.content.serializers import ContentItemCategorySerializer


class CustomPageAPIViewset(PagesAPIViewSet):
    # the order is important...wagtail filters come last
    filter_backends = [
        SMSContentItemFilterSet,
        TagFilter,
        ClientFilter,
        ContentSequenceFilter,
        FacilityFilter,
        CategoryFilter,
        ContentFilter,
        FieldsFilter,
        ChildOfFilter,
        AncestorOfFilter,
        DescendantOfFilter,
        OrderingFilter,
        TranslationOfFilter,
        LocaleFilter,
        SearchFilter,  # must be last
    ]
    known_query_parameters = PagesAPIViewSet.known_query_parameters.union(
        [
            "offer_code",
            "initial_content",
            "current_sequence_number",
            "tag",
            "category",
            "category_name",
            "client_id",
            "facility_id",
            "exclude_category",
            "exclude_content",
        ]
    )

    def detail_view(self, request, pk=None, slug=None):
        param = pk
        if slug is not None:
            self.lookup_field = "slug"
            param = slug
        return super().detail_view(request, param)

    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            path("", cls.as_view({"get": "listing_view"}), name="listing"),
            path("<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"),
            path("<slug:slug>/", cls.as_view({"get": "detail_view"}), name="detail"),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]


class ContentItemCategoryViewSet(BaseView):
    queryset = ContentItemCategory.objects.all()
    serializer_class = ContentItemCategorySerializer
    filterset_class = ContentItemCategoryFilter
