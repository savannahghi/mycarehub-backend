from django.contrib import admin

from mycarehub.common.models.common_models import AuditLog

from .models import Facility, Organisation, Program


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


@admin.register(AuditLog)
class AuditLogAdmin(BaseAdmin):
    pass


@admin.register(Program)
class ProgramAdmin(BaseAdmin):
    pass
