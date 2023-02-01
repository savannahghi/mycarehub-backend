from django.core.paginator import Paginator
from wagtail.documents.views.documents import IndexView


class CustomDocumentIndexView(IndexView):
    """
    Modifies the `get_context_data` to only show documents in an organisation
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filtered_documents = []
        for document in context["documents"]:
            if document.organisation == self.request.user.organisation:
                filtered_documents.append(document)

        paginator = Paginator(filtered_documents, per_page=20)
        documents = paginator.get_page(self.request.GET.get("p"))

        context.update(
            {
                "documents": documents,
            }
        )

        return context
