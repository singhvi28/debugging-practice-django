from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from spy import call_count, call_log, record_call, reset_spy


@csrf_exempt
@require_http_methods(["POST"])
def notify(request, channel):
    record_call(channel)
    return JsonResponse({"channel": channel, "sent": True})


@csrf_exempt
@require_http_methods(["POST"])
def reset(request):
    reset_spy()
    return JsonResponse({"reset": True})


@require_http_methods(["GET"])
def debug_spy(request):
    return JsonResponse({"count": call_count(), "log": call_log()})
