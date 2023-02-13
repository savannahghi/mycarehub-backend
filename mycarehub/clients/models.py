from django.db.models import PROTECT, CharField, ForeignKey
from django.db.models.fields import DateField
from django.utils.translation import gettext_lazy as _

from mycarehub.common.models import AbstractBase
from mycarehub.users.models import GenderChoices
from mycarehub.utils.general_utils import default_program


class Client(AbstractBase):
    name = CharField(_("Name of Client"), blank=True, max_length=255)
    gender = CharField(choices=GenderChoices.choices, max_length=16, null=True, blank=True)
    date_of_birth = DateField(null=True, blank=True)
    program = ForeignKey(
        "common.Program", on_delete=PROTECT, default=default_program, related_name="clients"
    )
