from leads.models import Lead


class LeadRepository:
    @staticmethod
    def create(data):
        return Lead.objects.create(**data)

    @staticmethod
    def get_by_email(email):
        return Lead.objects.filter(email__iexact=email).first()

    @staticmethod
    def exists_by_email(email):
        return Lead.objects.filter(email__iexact=email).exists()
