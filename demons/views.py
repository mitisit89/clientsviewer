import json

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from clientsviewer.settings import BASE_DIR

from .serializers import MemoryCheckerSerializer


@api_view(["GET"])
def get_memory_left(request: Request) -> Response:
    """
    Assept get request,returns json array with date and amount of memory available on the host
    """
    with open(f"{BASE_DIR}/logs.json", "r", encoding="utf-8") as f:
        memory_log = json.load(f)
        result = MemoryCheckerSerializer(memory_log)
        return Response(result.data)
