from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.enums import TextChoices
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from wagtail.snippets.models import register_snippet

from mycarehub.common.models import AbstractBase
from mycarehub.common.models.common_models import Facility


class FlavourChoices(TextChoices):
    PRO = "PRO", _("PRO")
    CONSUMER = "CONSUMER", _("CONSUMER")


class Languages(TextChoices):
    en = "en", "English"
    sw = "sw", "Swahili"


class ClientType(models.TextChoices):
    """
    The client types shown below can be expanded over time:

        - PMTCT: Prevention of mother-to-child transmission;
        all pregnant and breastfeeding women living with HIV.
        Exit when baby turns 2 years.

        - OTZ:  Operation Tripple Zero – for Zero Missed Appointments, zero
        missed Drugs and Zero Viral Load – all HIV positive persons aged
        between 0-19 years

        - OTZ Plus: All women aged between 10-24 years who are pregnant or
        breastfeeding. Exit when baby turns 2 years

        - HVL: High Viral Load – All HIV positive clients with a viral load
        >1,000 copies per ml. Exit when VL is <1,000 copies/ml

        - OVC: Orphans and Vulnerable Children – all children and
        adolescents aged 0-17 years who are enrolled with an OVC partner.
        Exit when they 18 years

        - DREAMS: Determined, Resilient, Empowered, AIDS-free, mentored and
        Safe – all HIV positive 9-24 year old women enroll with a DREAMS
        partner. Exit when they turn 25 years

        - High Risk Clients: all paediatric patients 0-4 yrs, all 0-4 year
        olds with a HIV negative guardian, all clients with low viremia
        (50-999 copies/ml). TI and new in the last 1 year, RTC in the last
        6 months.

        - Spouses of PMTCT mothers who have disclosed – exit when the
        baby turns 2 years

        - Youth: 20–24-year-olds both male and female. Exit when they turn
        25 years
    """

    PMTCT = "PMTCT", _("PMTCT")
    OTZ = "OTZ", _("OTZ")
    OTZ_PLUS = "OTZ_PLUS", _("OTZ Plus")
    HVL = "HVL", _("HVL")
    OVC = "OVC", _("OVC")
    DREAMS = "DREAMS", _("DREAMS")
    HIGH_RISK = "HIGH_RISK", _("High Risk Clients")
    SPOUSES = "SPOUSES", _("SPOUSES")
    YOUTH = "YOUTH", _("Youth")
    KENYAEMR = "KenyaEMR", _("Kenya EMR")


class Caregiver(AbstractBase):
    """
    A caregiver is a person who is assigned to a client.
    """

    class CaregiverType(models.TextChoices):
        FATHER = "FATHER", _("Father")
        MOTHER = "MOTHER", _("Mother")
        SIBLING = "SIBLING", _("Sibling")
        HEALTHCARE_PROFESSIONAL = (
            "HEALTHCARE_PROFESSIONAL",
            _("Healthcare Professional"),
        )

    first_name = models.TextField()
    last_name = models.TextField()
    caregiver_type = models.CharField(max_length=64, choices=CaregiverType.choices)
    phone_number = models.TextField(null=True, blank=True, max_length=14)


@register_snippet
class Client(AbstractBase):
    """
    A client is a patient or non-professional end user.
    """

    client_types = ArrayField(
        models.CharField(
            max_length=64,
        ),
        null=False,
        blank=True,
        default=list,
    )

    # a client is a user, hence the one-to-one mapping
    # however, the client can be created (e.g via an integration) before
    # the user is invited. This is the reason why this field is nullable.
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # a client must have an enrollment date.
    # if it is not known, integration code should set a sensible default.
    enrollment_date = models.DateTimeField(null=False, blank=False, default=timezone.now)

    # the client's FHIR health record ID
    # optional because the client's FHIR health record is created after the client is enrolled
    fhir_patient_id = models.TextField(null=True, blank=True, unique=True)

    # the client's EMR ID
    # optional because it can be updated after the client is added e.g via an integration
    emr_health_record_id = models.TextField(null=True, blank=True, unique=True)

    # each client is assigned to a facility
    current_facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )

    # a client can be assigned a community health volunteer
    chv = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name="client_chvs",
        null=True,
        blank=True,
    )

    # a client can be assigned a treatment buddy
    treatment_buddy = models.TextField(null=True, blank=True)

    # a client should only be invited to the platform after they have been
    # counselled
    counselled = models.BooleanField(default=False)

    languages = ArrayField(
        models.CharField(
            max_length=150,
            choices=Languages.choices,
        ),
        null=True,
        blank=True,
    )
    caregiver = models.OneToOneField(
        Caregiver,
        related_name="client_caregiver",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.user.name} ({self.client_types})"
            if self.user
            else f"{self.client_types} client"
        )


@register_snippet
class ClientFacility(AbstractBase):
    """
    ClientFacility tracks a client's assigned facilities and changes over time.
    """

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
    notes = models.TextField(default="-")
    assigned = models.DateTimeField(default=timezone.now)
    transferred_out = models.DateTimeField(null=True, blank=True)

    class Meta(AbstractBase.Meta):
        unique_together = (
            "client",
            "facility",
        )
