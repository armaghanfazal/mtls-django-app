from rest_framework import serializers


class DataLogSubmitSerializer(serializers.Serializer):
    level = serializers.ChoiceField(
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help_text="Log level"
    )
    message = serializers.CharField(
        max_length=5000,
        allow_blank=True,
        required=False,
        help_text="Log message"
    )

    def validate_level(self, value):
        return value.upper()
