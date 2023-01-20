from django.db import models

from mycarehub.clients.models import Client
from mycarehub.common.models import AbstractBase, Program
from mycarehub.utils.general_utils import default_program

from .models import ContentItem


class ContentInteraction(AbstractBase):
    """
    This is an abstract base model that is used to hold common fields and
    behaviours for content interactions e.g like, save, share etc.
    """

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    content_item = models.ForeignKey(ContentItem, on_delete=models.PROTECT)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, default=default_program)

    class Meta:
        abstract = True


class ContentLike(ContentInteraction):
    """
    When a user likes a content item, an entry is added here and the cached
    count on the content item is updated.

    When a user unlikes a content item, the entry here is removed and the cached
    count on the content item is updated.

    These updates should be performed in a transaction - with special care
    taken to ensure that the incrementing and decrementing of the cached counts
    is not prone to race conditions.
    """

    class Meta:
        unique_together = (
            "client",
            "content_item",
        )


class ContentBookmark(ContentInteraction):
    """
    When a user bookmarks (saves or pins) a content item, an entry is added
    here and the cached count on the content item is updated.

    When a user removes a bookmark, the entry here is removed and the cached
    count on the content item is updated.

    These updates should be performed in a transaction - with special care
    taken to ensure that the incrementing and decrementing of the cached counts
    is not prone to race conditions.
    """

    class Meta:
        unique_together = (
            "client",
            "content_item",
        )


class ContentShare(ContentInteraction):
    """
    When a user shares a content item, an entry is added
    here and the cached count on the content item is updated.

    There is no notion of "unsharing".

    These updates should be performed in a transaction - with special care
    taken to ensure that the incrementing and decrementing of the cached counts
    is not prone to race conditions.
    """

    class Meta:
        unique_together = (
            "client",
            "content_item",
        )


class ContentView(ContentInteraction):
    """
    When a user views a content item, an entry is added
    here and the cached count on the content item is updated.

    There is no notion of "unviewing".

    These updates should be performed in a transaction - with special care
    taken to ensure that the incrementing and decrementing of the cached counts
    is not prone to race conditions.
    """

    class Meta:
        unique_together = (
            "client",
            "content_item",
        )
