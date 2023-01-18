from typing import Any

from rest_framework import parsers, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .renderers import UserJSONRenderer
from .serializers import (LoginUserSerializer, LogoutSerializer,
                          RegistrationUserSerializer, UserSerializer)


class RegistrationApi(APIView):
    permission_classes = (AllowAny,)
    renderer_classes= (UserJSONRenderer,)
    serializer_class = RegistrationUserSerializer
    parser_classes=(parsers.MultiPartParser,parsers.FileUploadParser)

    def post(self, request: Request) -> Response:
        """Return user response after a successful registration."""
        user_request = request.data
        serializer = self.serializer_class(data=user_request)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginApi(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginUserSerializer

    def post(self, request: Request) -> Response:
        """Return user after login."""
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateApi(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    lookup_url_kwarg = "id"
    parser_classes = [
        parsers.MultiPartParser,
    ]

    def get(
        self, request: Request, *args: type[Any], **kwargs: dict[str, Any]
    ) -> Response:
        """Get request"""
        serializer = self.serializer_class(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(
        self, request: Request, *args: type(Any), **kwargs: dict[str, Any]
    ) -> Response:
        serializer_data = request.data.get("user", {})
        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Validate token and save."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
