from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from credentials import get_secret, rotate_secret

EXPECTED_AFTER_ROTATE = "secret-v2"


@csrf_exempt
@require_http_methods(["POST"])
def rotate(request):
    rotate_secret(EXPECTED_AFTER_ROTATE)
    return JsonResponse({"rotated": True, "secret": EXPECTED_AFTER_ROTATE})


@csrf_exempt
@require_http_methods(["POST"])
def submit(request):
    if get_secret() != EXPECTED_AFTER_ROTATE:
        return JsonResponse({"detail": "access denied"}, status=403)
    return JsonResponse({"status": "accepted"})
