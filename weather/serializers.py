from rest_framework.serializers import CharField, DateField, Serializer


class PostWeatherSerializer(Serializer):
    day = DateField(required=True, style={"dt": "yyyy-mm-dd"})
    city = CharField(required=True, max_length=15)
