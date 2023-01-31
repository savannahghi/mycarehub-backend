from django.core.paginator import Paginator
from wagtail.documents.views.documents import IndexView
from wagtail.documents.views.multiple import AddView


class CustomDocumentIndexView(IndexView):
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


class CustomDocumentAddView(AddView):
    def save_object(self, form):
        document = form.save(commit=False)
        document.uploaded_by_user = self.request.user
        document.organisation = self.request.user.organisation
        document.save()
        return document
