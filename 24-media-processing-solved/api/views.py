import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api import store
def b(r):
 try:return json.loads(r.body or b'{}')
 except (ValueError,UnicodeDecodeError):return {}
@require_http_methods(['GET'])
def media(r,i):
 x=store.get(i)
 if not x:return JsonResponse({'detail':'Media not found'},status=404)
 if x['owner']!=r.headers.get('X-User','alice'):return JsonResponse({'detail':'Forbidden'},status=403)
 return JsonResponse(x)
@csrf_exempt
@require_http_methods(['POST'])
def process(r,i):
 x=store.process(i,b(r).get('ok',False))
 return JsonResponse(x) if x else JsonResponse({'detail':'Media not found'},status=404)
@require_http_methods(['GET'])
def signed(r,i):return JsonResponse(store.signed(i))
@require_http_methods(['GET'])
def listing(r):return JsonResponse(store.page(int(r.GET.get('limit','2')),r.GET.get('cursor')),safe=False)
