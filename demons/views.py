import json

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from clientsviewer.settings import BASE_DIR

from .serializers import MemoryCheckerSerializer


class GetMemoryLeft(APIView):
    """
    Accept get request,returns json array with date and amount of memory available on the host.
    Login requered"
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MemoryCheckerSerializer

    def get(self, request: Request) -> Response:
        with open(f"{BASE_DIR}/logs.json", "r", encoding="utf-8") as f:
            memory_log = json.load(f)
            result = MemoryCheckerSerializer(memory_log)
            return Response(result.data)
