import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api import store
def b(r):
 try:return json.loads(r.body or b'{}')
 except (ValueError,UnicodeDecodeError):return {}
@csrf_exempt
@require_http_methods(['POST'])
def create(r):
 x=b(r);amount=x.get('amount',0);key=r.headers.get('Idempotency-Key','')
 if not key:return JsonResponse({'detail':'Invalid body'},status=400)
 return JsonResponse(store.create(r.headers.get('X-User','alice'),amount,key),status=201)
@csrf_exempt
@require_http_methods(['POST'])
def decide(r,i):
 x=store.decide(i,b(r).get('approved',False),r.headers.get('X-User','manager'))
 if x is None:return JsonResponse({'detail':'Expense not found'},status=404)
 if x=='conflict':return JsonResponse({'detail':'Already decided'},status=400)
 return JsonResponse(x)
@require_http_methods(['GET'])
def detail(r,i):
 x=store.get(i)
 if not x:return JsonResponse({'detail':'Expense not found'},status=404)
 return JsonResponse(x)
@require_http_methods(['GET'])
def total(r):return JsonResponse({'total':store.total(r.headers.get('X-User','alice'))})
