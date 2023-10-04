# type: ignore
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import RedirectView, TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.images.views.serve import ServeView

from mycarehub.common.views import AboutView, HomeView
from mycarehub.content.views import (
    CustomDocumentIndexView,
    CustomImageIndexView,
    CustomPageAPIViewset,
    SignedURLView,
    media_index,
)

urlpatterns = [
    path("sysadmin/", HomeView.as_view(), name="home"),
    re_path(
        r"^favicon\.ico$",
        RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico", permanent=True),
    ),
    path(
        "about/",
        AboutView.as_view(),
        name="about",
    ),
    path(settings.ADMIN_URL, admin.site.urls),
    path("users/", include("mycarehub.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("common/", include("mycarehub.common.urls", namespace="common")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
api_patterns = [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    # OAuth 2
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]
urlpatterns += api_patterns

# Open API Schema and automatic API documentation
urlpatterns += [
    path(
        "openapi",
        get_schema_view(
            title=settings.SITE_NAME,
            description=f"{settings.SITE_NAME} REST API",
            version=settings.API_VERSION,
            patterns=api_patterns,
        ),
        name="openapi-schema",
    ),
    path(
        "swagger/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="redoc",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


wagtail_api_router = WagtailAPIRouter("wagtailapi")
wagtail_api_router.register_endpoint("pages", CustomPageAPIViewset)
wagtail_api_router.register_endpoint("images", ImagesAPIViewSet)
wagtail_api_router.register_endpoint("documents", DocumentsAPIViewSet)

urlpatterns += [
    path("contentapi/", wagtail_api_router.urls, name="wagtail_content_api"),
    path("admin/images/", CustomImageIndexView.as_view(), name="wagtailimages-index"),
    path("admin/media/", media_index, name="wagtailmedia-index"),
    path("admin/documents/", CustomDocumentIndexView.as_view(), name="wagtaildocs-index"),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    re_path(
        r"^images/([^/]*)/(\d*)/([^/]*)/[^/]*$",
        ServeView.as_view(),
        name="wagtailimages_serve",
    ),
    path("content/", include(wagtail_urls), name="wagtail"),
    path("signed-url/", SignedURLView.as_view(), name="signed-url"),
]

urlpatterns += i18n_patterns(
    path("", include(wagtail_urls), name="wagtail"),
)
