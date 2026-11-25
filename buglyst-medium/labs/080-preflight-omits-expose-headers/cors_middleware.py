from django.http import HttpResponse

from helper import apply_cors_headers


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("origin", "")
        is_preflight = request.method == "OPTIONS"

        if is_preflight:
            response = HttpResponse(status=204)
        else:
            response = self.get_response(request)

        for key, value in apply_cors_headers(
            dict(response.headers),
            origin,
            is_preflight=is_preflight,
        ).items():
            response[key] = value

        return response
