from copy import deepcopy
_projects={}; _tasks={}; _next=1
def reset():
 global _projects,_tasks,_next; _projects={'p1':{'id':'p1','name':'Launch','owner':'alice','archived':False}}; _tasks={}; _next=1
def projects(include_archived=False): return deepcopy([p for p in _projects.values() if include_archived or not p['archived']])
def create(name,owner):
 global _next
 p={'id':f'p{_next}','name':name,'owner':owner,'archived':False}; _next+=1; _projects[p['id']]=p; return deepcopy(p)
def archive(pid):
 p=_projects.get(pid)
 if not p:return None
 p['archived']=True; return deepcopy(p)
def add_task(pid,title):
 if pid not in _projects:return None
 t={'id':f't{len(_tasks)+1}','project_id':pid,'title':title,'done':False,'version':1}; _tasks[t['id']]=t; return deepcopy(t)
def update(tid,title,version):
 t=_tasks.get(tid)
 if not t:return 'missing'
 if t['version']!=version:return 'conflict'
 t['title']=title;t['version']+=1;return deepcopy(t)
def page(limit,cursor):
 rows=sorted(_tasks.values(),key=lambda x:x['id']); start=int(cursor or 0); return {'items':deepcopy(rows[start:start+limit]),'next_cursor':str(start+limit) if start+limit<len(rows) else None}
reset()
