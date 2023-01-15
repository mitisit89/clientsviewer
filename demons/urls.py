from django.urls import path

from .views import GetMemoryLeft

urlpatterns = [path("check_memory", GetMemoryLeft.as_view())]
