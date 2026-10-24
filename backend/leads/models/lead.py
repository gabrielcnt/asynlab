from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone


class Source(models.TextChoices):
    INSTAGRAM = "instagram", "Instagram"
    GOOGLE = "google", "Google"
    DIRECT = "direct", "Direto"
    OTHER = "other", "Outro"


class Status(models.TextChoices):
    NEW = "new", "Novo"
    CONTACTED = "contacted", "Em contato"
    CONVERTED = "converted", "Convertido"
    DISCARDED = "discarded", "Descartado"


class Lead(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20)
    source = models.CharField(max_length=30, choices=Source.choices)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NEW)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_submission_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="unique_lower_email",
            )
        ]

    def __str__(self):
        return self.name
