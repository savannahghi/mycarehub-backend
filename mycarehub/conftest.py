import pytest
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.messages.storage.fallback import FallbackStorage
from django.utils import timezone
from faker import Faker
from model_bakery import baker
from taggit.models import Tag
from wagtail.models import Page, Site

from mycarehub.common.models import Facility, Program
from mycarehub.content.models import Author, ContentItem, ContentItemCategory, ContentItemIndexPage
from mycarehub.content.models.sms import SMSContentItem, SMSContentItemCategory, SMSContentItemTag
from mycarehub.content.wagtail_hooks import set_organisation_after_page_create
from mycarehub.home.models import HomePage
from mycarehub.users.models import User
from mycarehub.users.tests.factories import UserFactory

fake = Faker()

baker.generators.add(
    "wagtail.images.models.WagtailImageField", "model_bakery.random_gen.gen_image_field"
)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture(autouse=True)
def test_email_backend(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture
def program() -> Program:
    return baker.make(Program)


@pytest.fixture
def sms_category(program):
    return baker.make(
        SMSContentItemCategory,
        code="001032833390",
        name="TYPE 1 DIABETES",
        sequence_key=1,
        programs=[program],
    )


@pytest.fixture
def sms_tag(program):
    return baker.make(
        SMSContentItemTag,
        name="Lifestyle Education",
        programs=[program],
    )


@pytest.fixture
def user(program) -> User:
    return UserFactory(program=program)


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
def request_with_user(rf, django_user_model, user_with_all_permissions):
    url = settings.ADMIN_URL + "/common/organisation/add/"
    request = rf.get(url)
    request.user = user_with_all_permissions
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    return request


@pytest.fixture
def homepage(request_with_user):
    # get the root page
    site = Site.find_for_request(request_with_user)
    assert site is not None
    root = site.root_page
    assert root is not None

    # set up a home page
    home = HomePage(
        title="Home",
        slug="index",
    )
    root.add_child(instance=home)
    root.save_revision().publish()

    return home


@pytest.fixture
def content_item_index(homepage, program):
    # set up a content item index page
    content_item_index = ContentItemIndexPage(
        title="Content Item Index",
        slug="articles",
        intro="content",
        program=program,
    )
    homepage.add_child(instance=content_item_index)
    homepage.save_revision().publish()

    content_item_index.save_revision().publish()

    return content_item_index


@pytest.fixture
def facility():
    return baker.make(Facility)


@pytest.fixture
def content_item_with_tag_and_category(content_item_index, program, facility):
    # get a hero image
    hero = baker.make("content.CustomImage", _create_files=True)

    # set up a content item
    author = baker.make(Author)
    content_item = ContentItem(
        title="An article",
        slug="article-1",
        intro="intro",
        body="body",
        item_type="ARTICLE",
        date=timezone.now().date(),
        author=author,
        hero_image=hero,
        program=program,
    )
    content_item_index.add_child(instance=content_item)
    content_item_index.save_revision().publish()

    # add a category
    icon = baker.make("content.CustomImage", _create_files=True)
    cat = baker.make(ContentItemCategory, id=999_999, name="a-valid-category", icon=icon)
    content_item.categories.add(cat)
    content_item.save()
    assert ContentItem.objects.filter(categories__id=cat.pk).count() == 1

    # add a tag
    tag = baker.make(Tag, name="a-valid-tag")  # expect slug a-valid-tag
    content_item.tags.add(tag)
    content_item.save()

    content_item.facilities.add(facility)

    assert ContentItem.objects.filter(tags__name="a-valid-tag").count() == 1

    # sanity checks
    assert (
        Page.objects.all().public().live().count() >= 4
    )  # root, home, content index, content item
    assert ContentItem.objects.all().public().live().count() == 1

    # return the initialized content item
    content_item.save_revision().publish()
    return content_item


@pytest.fixture
def initial_sms_content_item(content_item_index, sms_category, sms_tag, request_with_user):
    """Initial SMS content item fixture."""
    initial_sms_content_item = SMSContentItem(
        content="This is some sample content for testing purposes",
        category=sms_category,
        tag=sms_tag,
    )

    content_item_index.add_child(instance=initial_sms_content_item)
    content_item_index.save_revision().publish()

    set_organisation_after_page_create(request=request_with_user, page=initial_sms_content_item)

    return initial_sms_content_item


@pytest.fixture
def sms_content_item(content_item_index, sms_category, sms_tag, request_with_user):
    """Subsequent SMS content item fixture."""
    sms_content_item = SMSContentItem(
        content="Hello is some sample content for testing purposes",
        category=sms_category,
        tag=sms_tag,
    )

    content_item_index.add_child(instance=sms_content_item)
    content_item_index.save_revision().publish()

    set_organisation_after_page_create(request=request_with_user, page=sms_content_item)

    return sms_content_item


def gen_rich_text_field():
    return fake.text()  # pragma: nocover


baker.generators.add("wagtail.fields.RichTextField", gen_rich_text_field)
