from django.db import models
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _

from mycarehub.clients.models import Client
from mycarehub.common.models import AbstractBase


class QuestionTypeChoices(TextChoices):
    TB_ASSESSMENT = "TB_ASSESSMENT", _("TB Assessment")
    VIOLENCE_ASSESSMENT = "VIOLENCE_ASSESSMENT", _("Violence Assessment")
    CONTRACEPTIVE_ASSESSMENT = "CONTRACEPTIVE_ASSESSMENT", _("Contraceptive Assessment")
    ALCOHOL_SUBSTANCE_ASSESSMENT = "ALCOHOL_SUBSTANCE_ASSESSMENT", _(
        "Alcohol and Substance Use Assessment"
    )


class ResponseCategoriesChoices(TextChoices):
    SINGLE_CHOICE = "SINGLE_CHOICE", _("Single Choice")
    MULTI_CHOICE = "MULTI_CHOICE", _("Multiple Choice")
    OPEN_ENDED = "OPEN_ENDED", _("Open Ended")


class ResponseTypesChoices(TextChoices):
    INTEGER = "INTEGER", _("Integer")
    TEXT = "TEXT", _("Text")
    DATE = "DATE", _("Date")


class ScreeningToolsQuestion(AbstractBase):
    """
    Screening Tools Questions Model defines the questions that are asked to the client
    response is a nullable field, it is only applicable to questions that have a
    response type SINGLE_CHOICE since the user is required to provide a response
    from the set of provided options.
    """

    question = models.TextField()
    tool_type = models.CharField(choices=QuestionTypeChoices.choices, max_length=32)
    response_choices = models.JSONField(null=True, blank=True)
    response_type = models.CharField(
        choices=ResponseTypesChoices.choices,
        max_length=32,
    )
    response_category = models.CharField(
        choices=ResponseCategoriesChoices.choices,
        max_length=32,
    )
    sequence = models.IntegerField()
    meta = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.question}"


class ScreeningToolsResponse(AbstractBase):
    """
    Screening Tools Responses Model defines the responses that are provided by the client
    response will be validate based on the response_type expected
    """

    question = models.ForeignKey(ScreeningToolsQuestion, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    response = models.TextField()

    def __str__(self) -> str:
        return f"{self.response}"
