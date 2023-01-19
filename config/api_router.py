from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

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
from mycarehub.users.api.views import UserAPIView

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
    path("users/<pk>", UserAPIView.as_view(), name="users-detail"),
    path(
        "users/",
        UserAPIView.as_view(),
        name="users-general",
    ),
    path("organisations/<pk>", OrganisationAPIView.as_view(), name="organisations-detail"),
    path(
        "organisations/",
        OrganisationAPIView.as_view(),
        name="organisations-general",
    ),
    path("programs/<pk>", ProgramAPIView.as_view(), name="programs-detail"),
    path(
        "programs/",
        ProgramAPIView.as_view(),
        name="programs-general",
    ),
]
