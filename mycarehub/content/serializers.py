from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from mycarehub.common.serializers.base_serializers import BaseSerializer

from .models import (
    ContentBookmark,
    ContentItem,
    ContentItemCategory,
    ContentLike,
    ContentShare,
    ContentView,
)


class ContentItemCategorySerializer(BaseSerializer):
    icon_url = serializers.SerializerMethodField()

    def get_icon_url(self, category):
        request = self.context.get("request")
        icon_url = category.icon.file.url
        return request.build_absolute_uri(icon_url)

    class Meta(BaseSerializer.Meta):
        model = ContentItemCategory
        fields = "__all__"


class ContentViewSerializer(BaseSerializer):
    def create(self, validated_data):
        with transaction.atomic():
            content_view = ContentView.objects.create(**validated_data)

            content_item = validated_data.get("content_item")
            ContentItem.objects.filter(id=content_item.id).update(view_count=F("view_count") + 1)

            return content_view

    class Meta(BaseSerializer.Meta):
        model = ContentView
        fields = "__all__"


class ContentShareSerializer(BaseSerializer):
    def create(self, validated_data):
        with transaction.atomic():
            content_share = ContentShare.objects.create(**validated_data)

            content_item = validated_data.get("content_item")
            ContentItem.objects.filter(id=content_item.id).update(share_count=F("share_count") + 1)

            return content_share

    class Meta(BaseSerializer.Meta):
        model = ContentShare
        fields = "__all__"


class ContentLikeSerializer(BaseSerializer):
    def create(self, validated_data):
        with transaction.atomic():
            content_like = ContentLike.objects.create(**validated_data)

            content_item = validated_data.get("content_item")
            ContentItem.objects.filter(id=content_item.id).update(like_count=F("like_count") + 1)

            return content_like

    class Meta(BaseSerializer.Meta):
        model = ContentLike
        fields = "__all__"


class ContentBookmarkSerializer(BaseSerializer):
    def create(self, validated_data):
        with transaction.atomic():
            content_bookmark = ContentBookmark.objects.create(**validated_data)

            content_item = validated_data.get("content_item")
            ContentItem.objects.filter(id=content_item.id).update(
                bookmark_count=F("bookmark_count") + 1
            )

            return content_bookmark

    class Meta(BaseSerializer.Meta):
        model = ContentBookmark
        fields = "__all__"
