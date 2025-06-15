from rest_framework import serializers

class NumerologyRequestSerializer(serializers.Serializer):
    firstname = serializers.CharField(
        max_length=255,
        required=True,
    )
    lastname = serializers.CharField(
        max_length=255,
        required=True,
    )
    birthdate = serializers.DateField(
        required=True,
    )
    language = serializers.CharField(
        max_length=5,
        default='en',
        required=False,
    )
