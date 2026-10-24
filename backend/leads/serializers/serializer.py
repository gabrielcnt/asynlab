import re

from rest_framework import serializers

from leads.models.lead import Source


class LeadSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    whatsapp = serializers.CharField(required=True)
    source = serializers.ChoiceField(choices=Source.choices, required=True)

    def validate_whatsapp(self, value):
        digits = re.sub(r"D", "", value)

        digits = digits.removeprefix("55")

        if len(digits) not in (10, 11):
            raise serializers.ValidationError(
                "Informe um número brasileiro válido com DDD."
            )

        if digits[0] == "0":
            raise serializers.ValidationError("O número informado é inválido.")

        return f"55{digits}"
