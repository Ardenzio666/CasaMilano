from django.contrib import admin

from .models import UserConsent


@admin.register(UserConsent)
class UserConsentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "consent_type",
        "accepted",
        "accepted_at",
        "policy_version",
    )

    list_filter = (
        "consent_type",
        "accepted",
        "policy_version",
        "accepted_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    readonly_fields = (
        "accepted_at",
    )

    ordering = (
        "-accepted_at",
    )