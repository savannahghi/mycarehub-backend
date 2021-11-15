import pytest
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from faker import Faker
from model_bakery import baker

from mycarehub.users.models import User
from mycarehub.users.tests.factories import UserFactory

fake = Faker()


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture(autouse=True)
def test_email_backend(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def user_with_all_permissions(user) -> User:
    all_perms = Permission.objects.all()
    for perm in all_perms:
        user.user_permissions.add(perm)
    user.save()
    return user


@pytest.fixture
def group_with_all_permissions() -> Group:
    group = baker.make(Group)
    all_perms = Permission.objects.all()
    for perm in all_perms:
        group.permissions.add(perm)

    group.save()
    return group


@pytest.fixture
def user_with_group(user, group_with_all_permissions) -> User:
    user.groups.add(group_with_all_permissions)
    user.save()
    return user


@pytest.fixture
def request_with_user(rf, django_user_model):
    url = settings.ADMIN_URL + "/common/organisation/add/"
    request = rf.get(url)
    user = baker.make(django_user_model)
    request.user = user
    return request


def gen_rich_text_field():
    return fake.text()  # pragma: nocover


baker.generators.add("wagtail.core.fields.RichTextField", gen_rich_text_field)
