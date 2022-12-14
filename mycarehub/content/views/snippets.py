from wagtail.snippets.views.snippets import SnippetViewSet

from mycarehub.content.filters import AuthorFilterSet, ContentItemCategoryFilterSet

class AuthorSnippetViewSet(SnippetViewSet):
    list_display = ["name", "avatar"]
    filterset_class = AuthorFilterSet

class ContentItemCategorySnippetViewSet(SnippetViewSet):
    list_display = ["name", "icon"]
    filterset_class = ContentItemCategoryFilterSet
