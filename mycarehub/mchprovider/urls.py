from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import MycarehubProvider

urlpatterns = default_urlpatterns(MycarehubProvider)
