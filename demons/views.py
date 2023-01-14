from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import MemoryCheckerSerializer
from .tasks import memory_check


@api_view(["GET"])
def get_memory_left(request: Request) -> Response:
    memory_data = memory_check.get()
    result = MemoryCheckerSerializer(memory_data, many=True).data
    return Response(result)
