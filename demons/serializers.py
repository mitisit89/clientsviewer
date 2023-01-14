from rest_framework import serializers


class MemoryCheckerSerializer(serializers.Serializer):
    content = serializers.JSONField()
