from typing import Any

from rest_framework import parsers
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView

from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegistrationUserSerializer,
    UserListSerializer,
    UserSerializer,
)


class RegistrationApi(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationUserSerializer
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request: Request) -> Response:
        """Return user response after a successful registration."""
        user_request = request.data
        serializer = self.serializer_class(data=user_request)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)


class LoginApi(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    parser_classes = (parsers.JSONParser,)

    def post(self, request: Request) -> Response:
        """Return user after login."""
        user = {
            "email": request.data.get("email", ""),
            "password": request.data.get("password", ""),
        }
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=HTTP_200_OK)


class UserList(ListAPIView):
    """Get all users. Login requered"""

    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserListSerializer
    parser_classes = (UserJSONRenderer,)

    def get_queryset(self):
        queryset = User.objects.prefetch_related("img").all()
        users: list[dict[str, Any]] = []
        for user in queryset:
            photo = user.img.all().first() or user.img.all().last()
            users.append(
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "surname": user.surname,
                    "sex": user.sex,
                    "birthday": user.birthday,
                    "photo": photo.photo,
                }
            )
        return users


class UpdateUser(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = UserSerializer

    def patch(
        self, request: Request, *args: type(Any), **kwargs: dict[str, Any]
    ) -> Response:
        """Partial update user data.Login requered"""
        # fix schema add user in schema
        serializer_data = request.data
        serializer = UserSerializer(request.user, data=serializer_data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class DeleteUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise HTTP_404_NOT_FOUND

    def delete(self, request: Request, email) -> Response:
        """Delete user by email.Login requered"""
        to_delete = self.get_object(email)
        to_delete.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Validate token and save."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=HTTP_204_NO_CONTENT)
