import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from register_helper import DuplicateEmailError, register, user_count


@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    body = json.loads(request.body)
    try:
        user = register(body["email"])
        return JsonResponse(user)
    except DuplicateEmailError:
        return JsonResponse({"detail": "email already registered"}, status=409)


@require_http_methods(["GET"])
def count_users(request):
    return JsonResponse({"count": user_count()})
