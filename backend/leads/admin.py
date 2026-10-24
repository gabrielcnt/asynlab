from django.contrib import admin

from leads.models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_filter = ("status", "source")

    search_fields = ("name", "email")

    fields = (
        "name",
        "email",
        "whatsapp",
        "source",
        "status",
        "notes",
        "last_submission_at",
    )
