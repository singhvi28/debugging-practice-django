from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def reports_collection(request):
    if request.method == "GET":
        return JsonResponse(store.list_reports(), safe=False)

    body = parse_json(request)
    title = body.get("title", "")
    owner = body.get("owner", "")
    if not title or not owner:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    report = store.create_report(title, owner)
    return JsonResponse(report, status=201)


@require_http_methods(["GET"])
def get_report(request, report_id: str):
    report = store.get_report(report_id)
    if report is None:
        return JsonResponse({"detail": "Report not found"}, status=404)
    return JsonResponse(report)


@csrf_exempt
@require_http_methods(["POST"])
def submit_report(request, report_id: str):
    report = store.submit_report(report_id)
    if report is None:
        return JsonResponse({"detail": "Report not found"}, status=404)
    return JsonResponse(report)


@csrf_exempt
@require_http_methods(["POST"])
def approve_report(request, report_id: str):
    report = store.get_report(report_id)
    if report is None:
        return JsonResponse({"detail": "Report not found"}, status=404)
    try:
        approved = store.approve_report(report_id)
    except ValueError as e:
        return JsonResponse({"detail": str(e)}, status=409)
    return JsonResponse(approved)

@csrf_exempt
@require_http_methods(["POST"])
def add_line_item(request, report_id: str):
    if store.get_report(report_id) is None:
        JsonResponse({"detail": "Report not found"}, status=404)

    body = parse_json(request)
    description = body.get("description", "")
    if not description:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    amount = body.get("amount")
    if amount is None:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    result = store.add_line_item(report_id, description, float(amount))
    if result is None:
        return JsonResponse({"detail": "Report not found"}, status=404)
    return JsonResponse(result) 

