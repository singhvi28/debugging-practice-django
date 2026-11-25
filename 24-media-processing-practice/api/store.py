from copy import deepcopy
_m={};_cache={}
def reset():
 global _m,_cache;_m={'m1':{'id':'m1','owner':'alice','status':'queued','attempts':0,'url':None}};_cache={}
def get(i):return deepcopy(_m.get(i))
def process(i,ok):
 x=_m.get(i)
 if not x:return None
 x['attempts']+=1;x['status']='ready' if ok else ('failed' if x['attempts']>=2 else 'queued');x['url']='https://cdn/'+i if ok else None;return deepcopy(x)
def signed(i):
 if i in _cache:return _cache[i]
 x={'url':'https://cdn/'+i,'expires_in':300};_cache[i]=x;return deepcopy(x)
def page(limit,cursor):
 rows=list(_m.values());start=int(cursor or 0);return {'items':deepcopy(rows[start:start+limit]),'next_cursor':str(start+limit) if start+limit<len(rows) else None}
reset()
