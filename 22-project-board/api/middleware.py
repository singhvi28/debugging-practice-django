from django.http import JsonResponse
class AuthMiddleware:
 def __init__(self,get_response): self.get_response=get_response
 def __call__(self,r):
  if r.method in ('POST','PATCH','DELETE') and r.path.startswith('/tasks') and r.headers.get('Authorization')!='Bearer secret-token': return JsonResponse({'detail':'Unauthorized'},status=401)
  return self.get_response(r)
