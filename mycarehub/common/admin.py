from django.contrib import admin

from mycarehub.common.models.common_models import Address, AuditLog, Contact

from .models import Facility, Organisation


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
        "created_by",
        "updated_by",
        "deleted_at",
    )
    exclude = (
        "created_by",
        "updated_by",
        "deleted_at",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.pk
            obj.updated_by = request.user.pk

        if change:
            obj.updated_by = request.user.pk

        obj.save()


@admin.register(Facility)
class FacilityAdmin(BaseAdmin):
    list_display = (
        "name",
        "mfl_code",
        "county",
    )
    list_filter = ("county",)


@admin.register(Organisation)
class OrganisationAdmin(BaseAdmin):
    pass


@admin.register(Address)
class AddressAdmin(BaseAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    pass


@admin.register(AuditLog)
class AuditLogAdmin(BaseAdmin):
    pass
