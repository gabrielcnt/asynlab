from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from leads.serializers.serializer import LeadSerializer
from leads.services.service import LeadService


@api_view(["POST"])
def submit_lead(request):
    serializer = LeadSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    LeadService.create_lead(serializer.validated_data)

    return Response(
        {"message": "Recebemos seus dados com sucesso."}, status=status.HTTP_200_OK
    )
