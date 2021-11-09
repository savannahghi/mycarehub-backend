# type: ignore
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, TemplateView
from graphene_django.views import GraphQLView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from mycarehub.common.views import AboutView, HomeView

from .graphql_auth import DRFAuthenticatedGraphQLView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "about/",
        AboutView.as_view(),
        name="about",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("mycarehub.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Our apps
    path("common/", include("mycarehub.common.urls", namespace="common")),
    # favicon
    re_path(
        r"^favicon\.ico$",
        RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico", permanent=True),
    ),
    path(
        "graphql", csrf_exempt(DRFAuthenticatedGraphQLView.as_view(graphiql=True)), name="graphql"
    ),
    # content management
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # re_path(r"authoring", include("mycarehub.content.urls")),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path(r"content", include(wagtail_urls), name="wagtail"),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
    # content management
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # re_path(r"content", include("mycarehub.content.urls")),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    # from wagtail.core import urls as wagtail_urls
    # re_path(r"", include(wagtail_urls)),
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
            template_name="swagger-ui.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
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
