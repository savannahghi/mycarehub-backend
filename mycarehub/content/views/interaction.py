from mycarehub.common.views.base_views import BaseView
from mycarehub.content.filters import (
    ContentBookmarkFilter,
    ContentLikeFilter,
    ContentShareFilter,
    ContentViewFilter,
)
from mycarehub.content.models import ContentBookmark, ContentLike, ContentShare, ContentView
from mycarehub.content.serializers import (
    ContentBookmarkSerializer,
    ContentLikeSerializer,
    ContentShareSerializer,
    ContentViewSerializer,
)


class ContentViewViewSet(BaseView):
    queryset = ContentView.objects.all()
    serializer_class = ContentViewSerializer
    filterset_class = ContentViewFilter


class ContentShareViewSet(BaseView):
    queryset = ContentShare.objects.all()
    serializer_class = ContentShareSerializer
    filterset_class = ContentShareFilter


class ContentLikeViewSet(BaseView):
    queryset = ContentLike.objects.all()
    serializer_class = ContentLikeSerializer
    filterset_class = ContentLikeFilter


class ContentBookmarkViewSet(BaseView):
    queryset = ContentBookmark.objects.all()
    serializer_class = ContentBookmarkSerializer
    filterset_class = ContentBookmarkFilter
