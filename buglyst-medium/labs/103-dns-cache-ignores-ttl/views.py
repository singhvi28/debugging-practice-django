from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import DnsRecord, reset, resolve

_RESOLVER_CALLS = 0
_RESOLVER_VERSION = 0


def _resolver(hostname: str) -> DnsRecord:
    global _RESOLVER_CALLS
    _RESOLVER_CALLS += 1
    if _RESOLVER_VERSION == 0:
        return DnsRecord(address="10.0.0.1", ttl_seconds=1)
    return DnsRecord(address="10.0.0.2", ttl_seconds=60)


def _reset_resolver_state() -> None:
    global _RESOLVER_CALLS, _RESOLVER_VERSION
    reset()
    _RESOLVER_CALLS = 0
    _RESOLVER_VERSION = 0


@csrf_exempt
@require_http_methods(["POST"])
def resolve_host(request):
    hostname = request.GET.get("hostname", "")
    now = float(request.GET.get("now", "0"))
    address = resolve(hostname, _resolver, now)
    return JsonResponse(
        {"hostname": hostname, "address": address, "resolver_calls": _RESOLVER_CALLS}
    )


@csrf_exempt
@require_http_methods(["POST"])
def rotate(request):
    global _RESOLVER_VERSION
    _RESOLVER_VERSION += 1
    return JsonResponse({"rotated": True, "version": _RESOLVER_VERSION})
