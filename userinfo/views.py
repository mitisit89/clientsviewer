from typing import Any, Optional

from django.conf import settings
from django.shortcuts import get_list_or_404
from rest_framework import parsers, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserModel
from .renderers import UserJSONRenderer
from .serializers import (LoginUserModelSerializer, LogoutSerializer,
                          RegistrationUserModelSerializer, UserModelSerializer)


class RegistrationApi(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationUserModelSerializer

    def post(self, request: Request) -> Response:
        """Return user response after a successful registration."""
        user_request = request.data.get("user", {})
        serializer = self.serializer_class(data=user_request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginApi(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LogoutSerializer

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
    serializer_class = UserModelSerializer
    lookup_url_kwarg = "id"
    parser_classes = [
        parsers.JSONParser,
        parsers.FormParser,
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
        serializer = UserModelSerializer(
            request.user, data=serializer_data, partial=True
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserModelSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
