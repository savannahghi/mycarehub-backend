from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mycarehub.clients.views import CaregiverViewSet, ClientFacilityViewSet, ClientViewSet
from mycarehub.common.views import FacilityViewSet, UserFacilityViewSet
from mycarehub.content.views import (
    ContentBookmarkViewSet,
    ContentItemCategoryViewSet,
    ContentLikeViewSet,
    ContentShareViewSet,
    ContentViewViewSet,
)
from mycarehub.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("facilities", FacilityViewSet)
router.register("user_facilities", UserFacilityViewSet)
router.register("clients", ClientViewSet)
router.register("client_facilities", ClientFacilityViewSet)
router.register("caregivers", CaregiverViewSet)
router.register("content_item_category", ContentItemCategoryViewSet)
router.register("content_view", ContentViewViewSet)
router.register("content_bookmark", ContentBookmarkViewSet)
router.register("content_like", ContentLikeViewSet)
router.register("content_share", ContentShareViewSet)

app_name = "api"
urlpatterns = router.urls
