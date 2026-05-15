# legal/models.py

from django.conf import settings
from django.db import models


class UserConsent(models.Model):
    PRIVACY_POLICY = "privacy_policy"
    NEWSLETTER_EVENTS = "newsletter_events"

    CONSENT_TYPES = [
        (PRIVACY_POLICY, "Privacy Policy"),
        (NEWSLETTER_EVENTS, "Newsletter eventi"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consents"
    )

    consent_type = models.CharField(
        max_length=50,
        choices=CONSENT_TYPES
    )

    accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(auto_now_add=True)

    policy_version = models.CharField(max_length=20, default="1.0")

    class Meta:
        verbose_name = "Consenso utente"
        verbose_name_plural = "Consensi utente"
        ordering = ["-accepted_at"]

    def __str__(self):
        return f"{self.user} - {self.consent_type} - {self.accepted}"