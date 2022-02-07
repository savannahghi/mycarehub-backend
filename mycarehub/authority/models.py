from django.contrib.auth import get_user_model
from django.db import models

from mycarehub.common.models import AbstractBase

User = get_user_model()


class AuthorityPermission(AbstractBase):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"


class AuthorityRole(AbstractBase):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(
        AuthorityPermission,
        related_name="role_permission",
    )
    users = models.ManyToManyField(
        User,
        related_name="user_roles",
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.name}"
