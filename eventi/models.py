from django.db import models

from django.db import models
from django.urls import reverse

from django.conf import settings

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ("private", "Evento Privato"),
        ("business", "Incontro Aziendale"),
        ("social", "Social Dining"),
        ("theme", "Cena a Tema"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="events/")
    event_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default="social")

    atmosphere = models.CharField(max_length=255, blank=True)
    ideal_for = models.CharField(max_length=255, blank=True)

    booking_url = models.URLField(blank=True)
    cta_text = models.CharField(max_length=100, blank=True, default="Prenota un posto")

    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["event_date", "order", "id"]

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        from django.utils import timezone
        return self.event_date < timezone.localdate()

    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.event_date >= timezone.localdate()
    
    @property
    def approved_comments(self):
        return self.comments.filter(is_approved=True)

    def get_absolute_url(self):
        return reverse("eventi:event_detail", kwargs={"slug": self.slug})


class EventImage(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="events/gallery/")
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Image for {self.event.title}"

    class Meta:
        ordering = ["order"]

class EventComment(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    # Per ora può essere NULL perché non hai ancora gli account attivi.
    # In futuro diventerà obbligatorio.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_comments",
        null=True,
        blank=True,
    )

    text = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Commento evento"
        verbose_name_plural = "Commenti eventi"

    def __str__(self):
        author = self.user.username if self.user else "Anonimo"
        return f"Commento di {author} su {self.event.title}"