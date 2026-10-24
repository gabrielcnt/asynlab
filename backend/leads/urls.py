from django.urls import path
from leads.views import submit_lead 

urlpatterns = [
    path("leads/", submit_lead, name="submit-lead")
]