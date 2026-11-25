from django.http import HttpResponse

from cors import origin_allowed


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin", "")

        if request.method == "OPTIONS":
            response = HttpResponse(status=204)
        else:
            response = self.get_response(request)

        if origin and origin_allowed(origin):
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "GET,OPTIONS"
            response["Vary"] = "Origin"

        return response
