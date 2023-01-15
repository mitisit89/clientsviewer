from django.urls import path

from .views import get_memory_left

urlpatterns = [path("check_memory", get_memory_left)]
