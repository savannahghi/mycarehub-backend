import datetime

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _

from mycarehub.clients.models import ClientType, FlavourChoices
from mycarehub.common.models import AbstractBase, Facility
from mycarehub.users.models import GenderChoices

User = get_user_model()


class QuestionTypeChoices(TextChoices):
    OpenEnded = "OPEN_ENDED", _("Open Ended")
    CloseEnded = "CLOSE_ENDED", _("Close Ended")


class ResponseValueChoices(TextChoices):
    String = "STRING", _("String")
    Number = "NUMBER", _("Number")
    Boolean = "BOOLEAN", _("Boolean")
    Date = "DATE", _("Date")
    Time = "TIME", _("Time")
    DateTime = "DATE_TIME", _("DateTime")


class Questionnaire(AbstractBase):
    """
    Questionnaire Model defines the survey that is asked to a user
    a survey can be of type Open Ended or Closed Ended. Open Ended surveys are
    surveys that don't have choices.
    Closed Ended surveys are surveys that have choices.
    Closed Ended surveys can have multiple responses.
    all surveys share response value type, which is a string, number, boolean, date, time, datetime
    """

    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(max_length=1000)
    valid_from = models.DateField(default=datetime.date.today)
    valid_days = models.IntegerField(default=0)
    valid_weeks = models.IntegerField(default=0)
    valid_months = models.IntegerField(default=0)
    valid_to = models.DateField(null=True, blank=True)
    frequency_days = models.IntegerField(default=0)
    frequency_weeks = models.IntegerField(default=0)
    frequency_months = models.IntegerField(default=0)
    next_survey_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class ScreeningTool(AbstractBase):
    """
    Screening Tool Model defines the screening tool that is asked to a client user
    they are a subset of the surveys.
    they contain properties that are specific to a screening tool type of questionnaire.
    they also contain properties that are common to a client user.
    """

    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    threshold = models.IntegerField(default=0)
    client_types = ArrayField(
        models.CharField(
            max_length=64,
            choices=ClientType.choices,
        ),
        null=True,
        blank=True,
        default=list,
    )
    genders = ArrayField(
        models.CharField(
            max_length=64,
            choices=GenderChoices.choices,
        ),
        null=True,
        blank=True,
        default=list,
    )
    min_age = models.IntegerField(default=14)
    max_age = models.IntegerField(default=25)

    def __str__(self):
        return "{}".format(self.questionnaire)


class Question(AbstractBase):
    """
    Question Model defines the questions that are asked to a user
    A question belongs to a questionnaire, a questionnaire  can have more than one.
    A question can be of type Open Ended or Closed Ended.
    Open Ended questions are surveys that don't have choices.
    Closed Ended questions are surveys that have choices.
    Closed Ended questions can have multiple responses.
    """

    text = models.TextField(max_length=5000, unique=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    question_type = models.CharField(
        max_length=20, choices=QuestionTypeChoices.choices, null=False
    )
    response_value_type = models.CharField(
        max_length=20, choices=ResponseValueChoices.choices, null=False
    )
    select_multiple = models.BooleanField(default=False)
    required = models.BooleanField(default=False)
    sequence = models.IntegerField(unique=True)

    def __str__(self):
        return "{}".format(self.text)


class QuestionInputChoice(AbstractBase):
    """
    Question Input Choice Model defines the choices that belong to a closed ended question
    A question can have more than one choice.
    based on the select_multiple property, a response can have multiple choices.
    score represents the score that is given to a choice.
    a score can be aggregated to a screening tool questionnaire and compared to the threshold.
    this will help with the logic of separating responses into positive or negative per user.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=100, null=False)
    value = models.CharField(max_length=100, null=False)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ("choice", "question")

    def __str__(self):
        return "{}:{}".format(self.choice, self.value)


class QuestionnaireResponse(AbstractBase):
    """
    Questionnaire Response Model defines the responses that a user gives to a questionnaire
    a response belongs to a questionnaire, a questionnaire can have more than one responses
    based on the number of question instances.
    All required questions must be answered.
    """

    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flavour = models.CharField(max_length=20, choices=FlavourChoices.choices, null=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

    def __str__(self):
        return "{} response for {}".format(self.questionnaire, self.user)


class ResponseInstance(AbstractBase):
    """
    Response Instance Model defines the instances of a question that a user gives a response to.
    The answer given is validated against the question settings.
    """

    questionnaire = models.ForeignKey(QuestionnaireResponse, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(max_length=1000)

    def __str__(self):
        return "{}".format(self.answer)
