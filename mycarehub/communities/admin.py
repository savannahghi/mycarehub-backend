from django.contrib import admin

from mycarehub.common.admin import BaseAdmin

from .models import Community, PostingHour


class PostingHourInline(admin.TabularInline):
    model = PostingHour


@admin.register(Community)
class CommunityAdmin(BaseAdmin):
    inlines = [PostingHourInline]


@admin.register(PostingHour)
class PostingHourAdmin(BaseAdmin):
    pass
