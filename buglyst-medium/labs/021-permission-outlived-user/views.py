import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from permissions import can_delete, revoke_user


@csrf_exempt
@require_http_methods(["POST"])
def revoke(request):
    body = json.loads(request.body)
    user_id = body.get("user_id")
    if not user_id or not revoke_user(user_id):
        return JsonResponse({"detail": "User not found"}, status=404)
    return JsonResponse({"revoked": user_id})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_resource(request, resource_id):
    x_user_id = request.headers.get("X-User-Id")
    if not can_delete(x_user_id):
        return JsonResponse({"detail": "Forbidden"}, status=403)
    return JsonResponse({"deleted": resource_id})
