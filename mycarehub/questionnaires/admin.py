from django.contrib.admin import site
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .models import (
    Question,
    QuestionInputChoice,
    Questionnaire,
    QuestionnaireResponse,
    ResponseInstance,
    ScreeningTool,
)


# Questionnaire Admin
class QuestionInputChoiceInline(NestedTabularInline):
    model = QuestionInputChoice
    extra = 0


class QuestionInline(NestedStackedInline):
    model = Question
    inlines = (QuestionInputChoiceInline,)
    extra = 0


class ScreeningToolInline(NestedStackedInline):
    model = ScreeningTool
    extra = 0


class QuestionnaireAdmin(NestedModelAdmin):
    inlines = (ScreeningToolInline, QuestionInline)


site.register(Questionnaire, QuestionnaireAdmin)


# Responses Admin
class ResponseInstanceAdminInline(NestedStackedInline):
    model = ResponseInstance
    extra = 0


class QuestionnaireResponseAdmin(NestedModelAdmin):
    inlines = (ResponseInstanceAdminInline,)


site.register(QuestionnaireResponse, QuestionnaireResponseAdmin)
