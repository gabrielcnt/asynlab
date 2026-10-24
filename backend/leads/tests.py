import threading

from django.contrib.auth import get_user_model
from django.db import connections
from rest_framework.test import APIClient, APITestCase

from leads.models.lead import Lead, Status


class LeadCreationTests(APITestCase):
    def test_create_valid_lead(self):
        payload = {
            "name": "Gabriel Vieira",
            "email": "gabrielcn96@email.com",
            "whatsapp": "21965876798",
            "source": "instagram",
        }

        response = self.client.post("/api/leads/", payload, format="json")
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 1)

        lead = Lead.objects.get(email="gabrielcn96@email.com")
        self.assertEqual(lead.name, "Gabriel Vieira")
        self.assertEqual(lead.email, "gabrielcn96@email.com")

    def test_reject_invalid_data(self):
        payload = {
            "name": "gabriel",
            "email": "email_invalido.com",
            "whatsapp": "398217",
            "source": "google",
        }

        response = self.client.post("/api/leads/", payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Lead.objects.count(), 0)

    def test_prevention_duplicates_email(self):
        payload = {
            "name": "gabriel",
            "email": "gabriel@email.com",
            "whatsapp": "21955555555",
            "source": "instagram",
        }

        response = self.client.post("/api/leads/", payload, format="json")

        self.assertEqual(response.status_code, 200)

        payload = {
            "name": "gabriel vieira",
            "email": "gabriel@email.com",
            "whatsapp": "21955555555",
            "source": "instagram",
        }

        response = self.client.post("/api/leads/", payload, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 1)

    def test_case_insensitive_email_comparison(self):
        payload = {
            "name": "gabriel vieira",
            "email": "gabriel@email.com",
            "whatsapp": "21955555555",
            "source": "instagram",
        }
        response = self.client.post("/api/leads/", payload, format="json")

        self.assertEqual(response.status_code, 200)

        payload = {
            "name": "gabriel vieira",
            "email": "Gabriel@Email.com",
            "whatsapp": "21955555555",
            "source": "instagram",
        }
        response = self.client.post("/api/leads/", payload, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 1)

    def test_update_last_submission_at(self):
        payload = {
            "name": "maria",
            "email": "maria@email.com",
            "whatsapp": "21966666666",
            "source": "direct",
        }

        response = self.client.post("/api/leads/", payload, format="json")
        self.assertEqual(response.status_code, 200)

        lead = Lead.objects.get(email="maria@email.com")

        time_first_request = lead.last_submission_at

        payload = {
            "name": "maria silva",
            "email": "maria@email.com",
            "whatsapp": "21988888888",
            "source": "direct",
        }

        response = self.client.post("/api/leads/", payload, format="json")
        self.assertEqual(response.status_code, 200)

        lead = Lead.objects.get(email="maria@email.com")
        time_second_request = lead.last_submission_at

        self.assertGreater(time_second_request, time_first_request)

    def test_preservation_original_data(self):
        payload = {
            "name": "maria",
            "email": "maria@email.com",
            "whatsapp": "21966666666",
            "source": "direct",
        }

        response = self.client.post("/api/leads/", payload, format="json")
        self.assertEqual(response.status_code, 200)

        payload = {
            "name": "paula",
            "email": "maria@email.com",
            "whatsapp": "21955555555",
            "source": "direct",
        }

        response = self.client.post("/api/leads/", payload, format="json")
        self.assertEqual(response.status_code, 200)

        lead = Lead.objects.get(email="maria@email.com")
        self.assertEqual(lead.name, "maria")
        self.assertEqual(lead.whatsapp, "5521966666666")

    def test_preservation_origin_and_status(self):
        payload = {
            "name": "julia",
            "email": "julia@email.com",
            "whatsapp": "21977777777",
            "source": "google",
        }

        response = self.client.post("/api/leads/", payload, format="json")
        self.assertEqual(response.status_code, 200)

        lead = Lead.objects.get(email="julia@email.com")

        lead.status = Status.CONTACTED

        lead.save()

        payload = {
            "name": "julia",
            "email": "julia@email.com",
            "whatsapp": "21977777777",
            "source": "instagram",
        }

        response = self.client.post("/api/leads/", payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(lead.status, "contacted")
        self.assertEqual(lead.source, "google")

    def test_responses_http(self):
        response = self.client.get("/api/leads/", format="json")

        self.assertEqual(response.status_code, 405)

        payload = {
            "name": "julia",
            "email": "julia@email.com",
            "whatsapp": "21977777777",
            "source": "instagram",
        }

        response = self.client.post("/api/leads/", payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"], "Recebemos seus dados com sucesso."
        )

    def test_lack_public_access_leads(self):
        response = self.client.get("/api/leads/1", format="json")

        self.assertEqual(response.status_code, 404)

    def test_permissions_django_admin(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)

        user = get_user_model().objects.create_user(
            "user_test", "teste@email.com", "12345678", is_staff=True
        )

        self.client.force_login(user)

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

    def test_simultaneous_request(self):
        responses = []

        def test_concurrent_request():
            try:
                payload = {
                    "name": "julia",
                    "email": "julia@email.com",
                    "whatsapp": "21977777777",
                    "source": "instagram",
                }

                user_client = APIClient()
                response = user_client.post("/api/leads/", payload, format="json")

                responses.append(response)
            finally:
                connections.close_all()

        thread_1 = threading.Thread(target=test_concurrent_request)
        thread_2 = threading.Thread(target=test_concurrent_request)

        thread_1.start()
        thread_2.start()

        thread_1.join()
        thread_2.join()

        self.assertEqual(len(responses), 2)

        for response in responses:
            self.assertEqual(response.status_code, 200)

        self.assertEqual(Lead.objects.filter(email="julia@email.com").count(), 1)
