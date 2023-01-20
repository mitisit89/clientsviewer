from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (DeleteUser, LoginApi, LogoutAPIView, RegistrationApi,
                    UpdateUser, UserList)

urlpatterns = [
    path("register/", RegistrationApi.as_view(), name="register_user"),
    path("login/", LoginApi.as_view(), name="login_user"),
    path("logout/", LogoutAPIView.as_view(), name="logout_user"),
    path("users/", UserList.as_view(), name="users"),
    path('user/update-info',UpdateUser.as_view(),name='update_user_info'),
    path('user/delete/<str:email>',DeleteUser.as_view(),name='delete_user'),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
