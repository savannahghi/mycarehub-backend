from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from mycarehub.clients.views import ClientAPIView
from mycarehub.common.views import (
    FacilityViewSet,
    OrganisationAPIView,
    ProgramAPIView,
    UserFacilityViewSet,
)
from mycarehub.content.views import (
    ContentBookmarkViewSet,
    ContentItemCategoryViewSet,
    ContentLikeViewSet,
    ContentShareViewSet,
    ContentViewViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("facilities", FacilityViewSet)
router.register("user_facilities", UserFacilityViewSet)
router.register("content_item_category", ContentItemCategoryViewSet)
router.register("content_view", ContentViewViewSet)
router.register("content_bookmark", ContentBookmarkViewSet)
router.register("content_like", ContentLikeViewSet)
router.register("content_share", ContentShareViewSet)

app_name = "api"
urlpatterns = router.urls + [
    path("organisations/<pk>/", OrganisationAPIView.as_view(), name="organisations-detail"),
    path(
        "organisations/",
        OrganisationAPIView.as_view(),
        name="organisations-general",
    ),
    path("programs/<pk>/", ProgramAPIView.as_view(), name="programs-detail"),
    path(
        "programs/",
        ProgramAPIView.as_view(),
        name="programs-general",
    ),
    path("clients/<pk>/", ClientAPIView.as_view(), name="clients-detail"),
    path(
        "clients/",
        ClientAPIView.as_view(),
        name="clients-general",
    ),
]
