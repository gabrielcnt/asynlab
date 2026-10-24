from django.db import IntegrityError, transaction
from django.utils import timezone

from leads.repositories.repository import LeadRepository


class LeadService:
    @staticmethod
    def create_lead(data):
        data["email"] = data["email"].strip().lower()
        lead = LeadRepository.get_by_email(data["email"])
        if lead:
            lead.last_submission_at = timezone.now()
            lead.save(update_fields=["last_submission_at"])
            return lead

        try:
            with transaction.atomic():
                return LeadRepository.create(data)
        
        except IntegrityError:
            lead = LeadRepository.get_by_email(data["email"])

            if lead:
                lead.last_submission_at = timezone.now()
                lead.save(update_fields=["last_submission_at"])
                return lead

            raise
