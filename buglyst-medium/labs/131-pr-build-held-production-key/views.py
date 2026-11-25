import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from deploy import STAGING_SECRET, BuildContext, get_deploy_secret


@csrf_exempt
@require_http_methods(["POST"])
def resolve_secret(request):
    body = json.loads(request.body)
    context = BuildContext(
        is_pull_request=body["is_pull_request"],
        is_fork=body["is_fork"],
        target_branch=body["target_branch"],
    )
    secret = get_deploy_secret(context)
    return JsonResponse(
        {
            "secret": secret,
            "environment": "production" if secret != STAGING_SECRET else "staging",
        }
    )
