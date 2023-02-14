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
    ContentItemCategoryFilter,
    ContentSequenceFilter,
    FacilityFilter,
    TagFilter,
)
from mycarehub.content.models import ContentItemCategory
from mycarehub.content.serializers import ContentItemCategorySerializer


class CustomPageAPIViewset(PagesAPIViewSet):
    # the order is important...wagtail filters come last
    filter_backends = [
        TagFilter,
        ClientFilter,
        ContentSequenceFilter,
        FacilityFilter,
        CategoryFilter,
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
        ["tag", "category", "category_name", "client_id", "facility_id"]
    )


class ContentItemCategoryViewSet(BaseView):
    queryset = ContentItemCategory.objects.all()
    serializer_class = ContentItemCategorySerializer
    filterset_class = ContentItemCategoryFilter
