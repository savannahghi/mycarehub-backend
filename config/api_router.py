from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mycarehub.common.views import FacilityViewSet, UserFacilityViewSet
from mycarehub.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("facilities", FacilityViewSet)
router.register("user_facilities", UserFacilityViewSet)

app_name = "api"
urlpatterns = router.urls
