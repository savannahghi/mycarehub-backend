from django.contrib import admin
from django.contrib.admin.decorators import display

from mycarehub.common.admin import BaseAdmin

from .models import (
    Client,
    ClientFacility,
    Identifier,
    RelatedPerson,
    SecurityQuestion,
    SecurityQuestionResponse,
)


@admin.register(Identifier)
class IdentifierAdmin(BaseAdmin):
    pass


@admin.register(SecurityQuestion)
class SecurityQuestionAdmin(BaseAdmin):
    pass


@admin.register(SecurityQuestionResponse)
class SecurityQuestionResponseAdmin(BaseAdmin):
    pass


@admin.register(RelatedPerson)
class RelatedPersonAdmin(BaseAdmin):
    pass


@admin.register(Client)
class ClientAdmin(BaseAdmin):
    list_display = (
        "get_user_name",
        "client_type",
        "enrollment_date",
    )
    date_hierarchy = "enrollment_date"
    exclude = (
        "fhir_patient_id",
        "emr_health_record_id",
    )  # type: ignore

    @display(ordering="user__name", description="User")
    def get_user_name(self, obj):
        return obj.user.name if obj.user else "-"


@admin.register(ClientFacility)
class ClientFacilityAdmin(BaseAdmin):
    pass
