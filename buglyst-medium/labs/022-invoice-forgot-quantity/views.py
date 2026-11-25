import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from invoice import invoice_total


@csrf_exempt
@require_http_methods(["POST"])
def create_invoice(request):
    body = json.loads(request.body)
    lines = body["lines"]
    total = invoice_total(lines)
    return JsonResponse(
        {"customer_id": body["customer_id"], "lines": lines, "total": total}
    )
