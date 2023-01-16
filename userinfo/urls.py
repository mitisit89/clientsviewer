from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (LoginApi, LogoutAPIView, RegistrationApi,
                    UserRetrieveUpdateApi)

urlpatterns = [
    path("register/", RegistrationApi.as_view(), name="register_user"),
    path("login/", LoginApi.as_view(), name="login_user"),
    path("logout/", LogoutAPIView.as_view(), name="logout_user"),
    path("user/", UserRetrieveUpdateApi.as_view(), name="user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
