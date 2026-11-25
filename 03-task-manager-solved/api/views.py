from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def projects_collection(request):
    if request.method == "GET":
        search = request.GET.get("search")
        if not store.list_projects(search):
            return JsonResponse({"detail": "No projects found"}, status=404)
        return JsonResponse(store.list_projects(search), safe=False)

    body = parse_json(request)
    name = body.get("name", "")
    if not name:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    project = store.create_project(name)
    return JsonResponse(project, status=201)


@require_http_methods(["GET"])
def get_project(request, project_id: str):
    project = store.get_project(project_id)
    if project is None:
        return JsonResponse({"detail": "Project not found"}, status=404)
    return JsonResponse(project, safe=False)


@csrf_exempt
@require_http_methods(["GET", "POST"])
async def project_tasks(request, project_id: str):
    if request.method == "GET":
        if store.get_project(project_id) is None:
            return JsonResponse({"detail": "Project not found"}, status=404)
        return JsonResponse(store.list_tasks(project_id), safe=False)

    if store.get_project(project_id) is None:
        return JsonResponse({"detail": "Project not found"}, status=404)

    body = parse_json(request)
    title = body.get("title", "")
    if not title:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    task = await store.save_task(project_id, title)
    return JsonResponse(task, status=201)


@csrf_exempt
@require_http_methods(["PATCH", "DELETE"])
def task_detail(request, task_id: str):
    if request.method == "DELETE":
        if not store.delete_task(task_id):
            return JsonResponse({"detail": "Task not found"}, status=404)
        return HttpResponse(status=204)

    body = parse_json(request)
    title = body.get("title")
    completed = body.get("completed")
    task = store.update_task(task_id, title, completed)
    if task is None:
        return JsonResponse({"detail": "Task not found"}, status=404)
    return JsonResponse(task)
