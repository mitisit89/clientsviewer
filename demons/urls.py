from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import get_memory_left


urlpatterns=[
        path('check_memory',get_memory_left)
        ]

urlpatterns = format_suffix_patterns(urlpatterns)
