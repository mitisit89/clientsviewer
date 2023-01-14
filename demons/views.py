import json

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import MemoryCheckerSerializer
from clientsviewer.settings import BASE_DIR
@api_view(["GET"])
def get_memory_left(request: Request) -> Response:
    """
    Assept get Request,returns json array with date and amount of memory available on the host  
    """
    try:
        memory_logs = open(f'{BASE_DIR}/logs.json','r',encoding='utf-8')
        f=json.load(memory_logs)
        result = MemoryCheckerSerializer(f)
        return Response(result.data)
    except ValueError as e:
        pass
    finally:
        memory_logs.close()
