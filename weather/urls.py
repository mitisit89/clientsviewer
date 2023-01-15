from django.urls import path

from .views import GetWeather

urlpatterns = [path("get_weather", GetWeather.as_view(), name="get_weather")]
