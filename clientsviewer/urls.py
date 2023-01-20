from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from demons import urls as demons_urls
from userinfo import urls as userinfo_urls
from weather import urls as weather_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/schema/", SpectacularAPIView.as_view(  custom_settings={'COMPONENT_SPLIT_REQUEST': True}), name="schema"),
    path(
        "docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("", include(userinfo_urls)),
    path("", include(demons_urls)),
    path("", include(weather_urls)),
]
