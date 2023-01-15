from rest_framework import serializers


class MemoryCheckerSerializer(serializers.Serializer):
    content = serializers.ListField(
        child=serializers.CharField(),
    )
