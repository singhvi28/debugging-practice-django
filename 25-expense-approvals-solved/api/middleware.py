from django.http import JsonResponse
class AuthMiddleware:
 def __init__(self,g):self.g=g
 def __call__(self,r):
  if r.method=='POST' and r.path.startswith('/expenses') and r.headers.get('Authorization')!='Bearer secret-token':return JsonResponse({'detail':'Unauthorized'},status=401)
  return self.g(r)
