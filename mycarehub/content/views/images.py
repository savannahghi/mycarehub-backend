from django.core.paginator import Paginator
from wagtail.images.views.images import IndexView


class CustomImageIndexView(IndexView):
    """
    Modifies the `get_context_data` to only show images in an organisation
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filtered_images = []
        for image in context["images"]:
            if image.organisation == self.request.user.organisation:
                filtered_images.append(image)

        entries_per_page = self.get_num_entries_per_page()
        paginator = Paginator(filtered_images, per_page=entries_per_page)
        images = paginator.get_page(self.request.GET.get("p"))

        context.update(
            {
                "images": images,
            }
        )

        return context
