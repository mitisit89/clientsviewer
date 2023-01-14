from rest_framework import serializers



class MemoryCheckerSerializer(serializers.Serializer):
    data=serializers.JSONField()
