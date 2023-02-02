import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostWeatherSerializer


class WeatherHandler:
    weather_api_url: str = "https://api.open-meteo.com/v1/forecast"
    weather_api_geo_coords_url: str = "https://geocoding-api.open-meteo.com/v1/search?"

    def __init__(self, day: str, city: str) -> None:
        self.day = day
        self.city = city.strip().lower()

    def get_geo_coords(self) -> list[float, ...]:
        params = {"name": str(self.city), "count": 1}
        req = requests.get(
            self.weather_api_geo_coords_url, params=params, timeout=10
        ).json()
        data = (req.get("results")[0].get(key) for key in ("latitude", "longitude"))
        return data

    def get_forecast(self) -> dict:
        latitude, longitude = self.get_geo_coords()
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m",
            "timezone": "auto",
            "start_date": self.day,
            "end_date": self.day,
        }
        data = requests.get(url=self.weather_api_url, params=params, timeout=10).json()
        return data


class GetWeather(APIView):
    """
    Endpoint receives a json object containing a user-defined date in format year-month-day and a city name.
    In response comes a json object containing weather data from external api.
    Login requered.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = PostWeatherSerializer

    def post(self, request: Request, format="json") -> Response:
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            day, city = (
                serialized_data.validated_data.get(key) for key in ("day", "city")
            )
            forecast = WeatherHandler(day=day, city=city)
            return Response(forecast.get_forecast(), status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
