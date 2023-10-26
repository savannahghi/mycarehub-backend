from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from wagtail.admin.views.account import LoginView

from mycarehub.common.views import ApprovedMixin
from mycarehub.content.models.models import ContentItemIndexPage

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, ApprovedMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, ApprovedMixin, RedirectView):
    permanent = False
    permission_required = "users.can_view_dashboard"

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class CustomLoginView(LoginView):
    """
    Modifes `get_success_url` to redirect users to the program index page.
    """

    def get_success_url(self):
        user = self.request.user

        # we show the first index page created for the current user's program
        index_page = (
            ContentItemIndexPage.objects.filter(program=user.program).order_by("id").first()
        )
        return reverse("wagtailadmin_explore", kwargs={"parent_page_id": index_page.id})


def login_redirect(request):
    user = request.user

    # we show the first index page created for the current user's program
    index_page = ContentItemIndexPage.objects.filter(program=user.program).order_by("id").first()
    return reverse("wagtailadmin_explore", kwargs={"parent_page_id": index_page.id})
