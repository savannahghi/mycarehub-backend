from wagtail.snippets.views.snippets import IndexView, SnippetViewSet

from mycarehub.content.filters import AuthorFilterSet, ContentItemCategoryFilterSet
from mycarehub.content.models import Author, ContentItemCategory


class AuthorSnippetIndexView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        authors = Author.objects.filter(organisation=self.request.user.organisation).all()
        context["object_list"] = authors

        return context


class AuthorSnippetViewSet(SnippetViewSet):
    list_display = ["name", "avatar"]
    filterset_class = AuthorFilterSet
    index_view_class = AuthorSnippetIndexView


class ContentItemCategorySnippetIndexView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = ContentItemCategory.objects.filter(
            organisation=self.request.user.organisation
        ).all()
        context["object_list"] = categories

        return context


class ContentItemCategorySnippetViewSet(SnippetViewSet):
    list_display = ["name", "icon"]
    filterset_class = ContentItemCategoryFilterSet
    index_view_class = ContentItemCategorySnippetIndexView
