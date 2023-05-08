from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.vary import vary_on_headers
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.auth import PermissionPolicyChecker
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.models import popular_tags_for_model
from wagtail.models import Collection
from wagtailmedia.models import get_media_model
from wagtailmedia.permissions import permission_policy
from wagtailmedia.utils import paginate

permission_checker = PermissionPolicyChecker(permission_policy)


@permission_checker.require_any("add", "change", "delete")
@vary_on_headers("X-Requested-With")
def media_index(request):
    Media = get_media_model()

    # Get media files (filtered by user permission)
    media = permission_policy.instances_user_has_any_permission_for(
        request.user, ["change", "delete"]
    ).filter(organisation=request.user.organisation)

    # Ordering
    if request.GET.get("ordering") in ["title", "-title", "-created_at", "created_at"]:
        ordering = request.GET["ordering"]
    else:
        ordering = "-created_at"
    media = media.order_by(ordering)

    # Filter by collection
    current_collection = None
    collection_id = request.GET.get("collection_id")
    if collection_id:
        try:
            current_collection = Collection.objects.get(id=collection_id)
            media = media.filter(collection=current_collection)
        except (ValueError, Collection.DoesNotExist):  # pragma: no cover
            pass

    # Search
    query_string = None
    if "q" in request.GET:
        form = SearchForm(request.GET, placeholder=_("Search media files"))
        if form.is_valid():  # pragma: no cover
            query_string = form.cleaned_data["q"]
            media = media.search(query_string)
    else:
        form = SearchForm(placeholder=_("Search media"))

    # Filter by tag
    current_tag = request.GET.get("tag")
    if current_tag:
        try:
            media = media.filter(tags__name=current_tag)
        except AttributeError:
            current_tag = None

    # Pagination
    paginator, media = paginate(request, media)

    collections = permission_policy.collections_user_has_any_permission_for(
        request.user, ["add", "change"]
    )
    if len(collections) < 2:  # pragma: no cover
        collections = None

    # Create response
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "wagtailmedia/media/results.html"
            if WAGTAIL_VERSION >= (4, 0, 0)
            else "wagtailmedia/media/legacy/results.html",
            {
                "ordering": ordering,
                "media_files": media,
                "query_string": query_string,
                "is_searching": bool(query_string),
                "collections": collections,
            },
        )
    else:
        return render(
            request,
            "wagtailmedia/media/index.html"
            if WAGTAIL_VERSION >= (4, 0, 0)
            else "wagtailmedia/media/legacy/index.html",
            {
                "ordering": ordering,
                "media_files": media,
                "query_string": query_string,
                "is_searching": bool(query_string),
                "search_form": form,
                "popular_tags": popular_tags_for_model(Media),
                "current_tag": current_tag,
                "user_can_add": permission_policy.user_has_permission(request.user, "add"),
                "collections": collections,
                "current_collection": current_collection,
            },
        )
