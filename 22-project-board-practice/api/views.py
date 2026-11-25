import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api import store
def b(r):
 try:return json.loads(r.body or b'{}')
 except (ValueError,UnicodeDecodeError):return {}
@require_http_methods(['GET','POST'])
@csrf_exempt
def projects(r):
  if r.method=='GET': return JsonResponse(store.projects(True),safe=False)
  x=b(r); p=store.create(x.get('name',''),r.headers.get('X-User','alice')); return JsonResponse(p,status=201) if p['name'] else JsonResponse({'detail':'Invalid body'},status=400)
@csrf_exempt
@require_http_methods(['POST'])
def archive(r,pid):
 p=store.archive(pid); return JsonResponse(p) if p else JsonResponse({'detail':'Project not found'},status=404)
@csrf_exempt
@require_http_methods(['POST'])
def tasks(r,pid):
 x=store.add_task(pid,b(r).get('title','')); return JsonResponse(x,status=201) if x else JsonResponse({'detail':'Project not found'},status=404)
@require_http_methods(['GET'])
def task_list(r): return JsonResponse(store.page(int(r.GET.get('limit','2')),r.GET.get('cursor')),safe=False)
@csrf_exempt
@require_http_methods(['PATCH'])
def update(r,tid):
 x=b(r); result=store.update(tid,x.get('title',''),x.get('version',0))
 if result=='missing':return JsonResponse({'detail':'Task not found'},status=404)
 if result=='conflict':return JsonResponse({'detail':'Version conflict'},status=400)
 return JsonResponse(result)
