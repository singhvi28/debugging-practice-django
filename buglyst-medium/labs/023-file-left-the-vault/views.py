from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from vault import read_file


@require_http_methods(["GET"])
def get_file(request):
    path = request.GET.get("path")
    content = read_file(path)
    if content is None:
        return JsonResponse({"detail": "File not found"}, status=404)
    return JsonResponse({"path": path, "content": content})
