from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def notifications_collection(request):
    if request.method == "GET":
        return JsonResponse(store.list_notifications(), safe=False)

    body = parse_json(request)
    title = body.get("title", "")
    body_text = body.get("body", "")
    notification = store.create_notification(title, body_text)
    return JsonResponse(notification, status=201)


@require_http_methods(["GET"])
def unread_count(request):
    return JsonResponse({"unread_count": store.get_unread_count()})


@csrf_exempt
@require_http_methods(["POST"])
def mark_notification_read(request, notification_id: str):
    notification = store.mark_read(notification_id)
    if notification is None:
        return JsonResponse({"detail": "Notification not found"}, status=404)
    return JsonResponse({
        "notification": notification,
        "unread_count": store.get_unread_count(),
    })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def notification_detail(request, notification_id: str):
    if request.method == "GET":
        notification = store.get_notification(notification_id)
        return JsonResponse(notification, safe=False)

    notification = store.mark_read(notification_id)
    if notification is None:
        return JsonResponse({"detail": "Notification not found"}, status=404)
    return JsonResponse({
        "notification": notification,
        "unread_count": store.get_unread_count(),
    })


@csrf_exempt
@require_http_methods(["POST"])
def mark_all_read(request):
    updated = store.mark_all_read()
    return JsonResponse({
        "marked_read": updated,
        "unread_count": store.get_unread_count(),
    })
