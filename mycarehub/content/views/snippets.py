from wagtail.snippets.views.snippets import SnippetViewSet

from mycarehub.content.filters import (
    AuthorFilterSet,
    ContentItemCategoryFilterSet,
    SMSContentItemCategoryFilterSet,
    SMSContentItemTagFilterSet,
)


class AuthorSnippetViewSet(SnippetViewSet):
    list_display = ["name", "avatar", "get_programs"]
    filterset_class = AuthorFilterSet


class ContentItemCategorySnippetViewSet(SnippetViewSet):
    list_display = ["name", "icon", "get_programs"]
    filterset_class = ContentItemCategoryFilterSet


class SMSContentItemCategorySnippetViewSet(SnippetViewSet):
    list_display = ["code", "name", "sequence_key", "get_programs"]
    filterset_class = SMSContentItemCategoryFilterSet


class SMSContentItemTagSnippetViewSet(SnippetViewSet):
    list_display = ["name", "code", "get_programs"]
    filterset_class = SMSContentItemTagFilterSet
