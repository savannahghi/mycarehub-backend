from django.contrib import admin

from mycarehub.common.admin import BaseAdmin

from .models import (
    Caregiver,
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


@admin.register(Caregiver)
class CaregiverAdmin(BaseAdmin):
    pass


@admin.register(Client)
class ClientAdmin(BaseAdmin):
    pass


@admin.register(ClientFacility)
class ClientFacilityAdmin(BaseAdmin):
    pass
