from wagtail.admin.views.generic.chooser import ChooseView
from wagtail.admin.viewsets.chooser import ChooserViewSet


class AuthorChooseView(ChooseView):
    def get_object_list(self):
        return self.model_class.objects.filter(organisation=self.request.user.organisation).all()


class AuthorChooserViewSet(ChooserViewSet):
    model = "content.Author"
    choose_view_class = AuthorChooseView


author_chooser_viewset = AuthorChooserViewSet("author_chooser")
