from copy import deepcopy
_e={};_keys={};_next=1
def reset():
 global _e,_keys,_next;_e={};_keys={};_next=1
def create(user,amount,key):
 global _next
 if key in _keys:return deepcopy(_e[_keys[key]])
 x={'id':f'e{_next}','user':user,'amount':amount,'status':'pending','approver':None};_next+=1;_e[x['id']]=x;_keys[key]=x['id'];return deepcopy(x)
def decide(i,approved,approver):
 x=_e.get(i)
 if not x:return None
 if x['status']!='pending':return 'conflict'
 x['status']='approved' if approved else 'rejected';x['approver']=approver;return deepcopy(x)
def get(i):return deepcopy(_e.get(i))
def total(user):return sum(x['amount'] for x in _e.values() if x['user']==user and x['status']=='approved')
reset()
