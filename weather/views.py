import requests
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostWeatherSerializer


class GetWeather(APIView):
    """
    Endpoint receives a json object containing a user-defined date in format year-month-day and a city name. 
    In response comes a json object containing weather data from external api
    """

    weather_api_url: str = "https://api.open-meteo.com/v1/forecast?"
    weather_api_geo_coords_url: str = "https://geocoding-api.open-meteo.com/v1/search?"
    serializer_class = PostWeatherSerializer

    def post(self, request: Request, format="json") -> Response:
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            day, city = (
                serialized_data.validated_data.get(key) for key in ("day", "city")
            )
            lat, lot = self.get_geo_coords(city)
            print(lat, lot)
            forecast = self.get_forecast(day, lat, lot)
            return Response(forecast, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_geo_coords(self, location: str) -> tuple[float, ...]:
        url = f"{self.weather_api_geo_coords_url}name={location}&count=1"
        req = requests.get(url=url).json()
        coord = (req.get("results")[0].get(key) for key in ("latitude", "longitude"))
        return tuple(coord)

    def get_forecast(self, day: str, latitude: float, longitude: float) -> dict:
        url = f"{self.weather_api_url}latitude={latitude}&longitude={longitude}&hourly=temperature_2m&timezone=auto&start_date={day}&end_date={day}"
        return requests.get(url).json()
