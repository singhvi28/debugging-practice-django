import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api import store
def b(r):
 try:return json.loads(r.body or b'{}')
 except (ValueError,UnicodeDecodeError):return {}
@require_http_methods(['GET'])
def detail(r,i):
 x=store.get(i)
 if not x:return JsonResponse({'detail':'Shipment not found'},status=404)
 return JsonResponse(x)
@csrf_exempt
@require_http_methods(['POST'])
def status(r,i):
 x=store.move(i,b(r).get('status'))
 if x is None:return JsonResponse({'detail':'Shipment not found'},status=404)
 if x=='invalid':return JsonResponse({'detail':'Invalid transition'},status=400)
 return JsonResponse(x)
@csrf_exempt
@require_http_methods(['POST'])
def webhook(r,i):
 x=store.event(i,b(r).get('status'),r.headers.get('Event-Id',''))
 if x is None:return JsonResponse({'detail':'Shipment not found'},status=404)
 if x=='invalid':return JsonResponse({'detail':'Invalid transition'},status=400)
 return JsonResponse(x)
