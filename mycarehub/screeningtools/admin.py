from django.contrib import admin

from mycarehub.common.admin import BaseAdmin

from .models import ScreeningToolsQuestion, ScreeningToolsResponse


@admin.register(ScreeningToolsQuestion)
class ScreeningToolsQuestionAdmin(BaseAdmin):
    pass


@admin.register(ScreeningToolsResponse)
class ScreeningToolsResponseAdmin(BaseAdmin):
    pass
