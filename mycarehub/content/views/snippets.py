from wagtail.snippets.views.snippets import SnippetViewSet

from mycarehub.content.filters import AuthorFilterSet, ContentItemCategoryFilterSet


class AuthorSnippetViewSet(SnippetViewSet):
    list_display = ["name", "avatar", "get_programs"]
    filterset_class = AuthorFilterSet


class ContentItemCategorySnippetViewSet(SnippetViewSet):
    list_display = ["name", "icon", "get_programs"]
    filterset_class = ContentItemCategoryFilterSet
