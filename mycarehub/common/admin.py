from django.contrib import admin

from mycarehub.common.models.common_models import Address, AuditLog, Contact

from .models import Facility, FacilityAttachment, Organisation


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "created_by",
        "updated",
        "updated_by",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.pk
            obj.updated_by = request.user.pk

        if change:
            obj.updated_by = request.user.pk

        obj.save()


class FacilityAttachmentInline(admin.TabularInline):
    model = FacilityAttachment


@admin.register(Facility)
class FacilityAdmin(BaseAdmin):
    inlines = [FacilityAttachmentInline]
    list_display = (
        "name",
        "mfl_code",
        "county",
        "sub_county",
        "constituency",
        "ward",
        "registration_number",
        "keph_level",
    )
    list_filter = (
        "county",
        "operation_status",
        "keph_level",
        "facility_type",
        "owner_type",
    )


@admin.register(FacilityAttachment)
class FacilityAttachmentAdmin(BaseAdmin):
    pass


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
