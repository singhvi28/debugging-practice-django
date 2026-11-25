from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def courses_collection(request):
    if request.method == "GET":
        search = request.GET.get("search")
        return JsonResponse(store.list_courses(search), safe=False)

    body = parse_json(request)
    title = body.get("title", "")
    if not title:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    course = store.create_course(title)
    return JsonResponse(course, status=201)


@require_http_methods(["GET"])
def get_course(request, course_id: str):
    course = store.get_course(course_id)
    return JsonResponse(course, safe=False)


@require_http_methods(["GET"])
def list_enrollments(request, course_id: str):
    enrollments = store.list_enrollments(course_id)
    if enrollments is None:
        return JsonResponse({"detail": "Course not found"}, status=404)
    return JsonResponse(enrollments, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def enroll_student(request, course_id: str):
    course = store.get_course(course_id)
    if course is None:
        JsonResponse({"detail": "Course not found"}, status=404)

    body = parse_json(request)
    student_id = body.get("student_id", "")
    if not student_id:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    enrollment = store.enroll_student(course_id, student_id)
    return JsonResponse(enrollment, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_enrollment(request, enrollment_id: str):
    if not store.delete_enrollment(enrollment_id):
        return JsonResponse({"detail": "Enrollment not found"}, status=404)
    return HttpResponse(status=204)
