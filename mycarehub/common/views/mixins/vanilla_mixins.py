from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import View

User = get_user_model()


class ApprovedMixin(UserPassesTestMixin, PermissionRequiredMixin, View):
    permission_denied_message = "Permission Denied"

    def test_func(self):
        return self.request.user.is_authenticated
