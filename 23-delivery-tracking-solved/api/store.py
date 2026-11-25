from copy import deepcopy
_s={};_events=set()
def reset():
 global _s,_events;_s={'s1':{'id':'s1','owner':'alice','status':'created','history':['created']}};_events=set()
def get(i):return deepcopy(_s.get(i))
def move(i,status):
 x=_s.get(i)
 if not x:return None
 allowed={'created':'picked_up','picked_up':'in_transit','in_transit':'delivered'}
 if allowed.get(x['status'])!=status:return 'invalid'
 x['status']=status;x['history'].append(status);return deepcopy(x)
def event(i,status,event_id):
 if event_id in _events:return get(i)
 _events.add(event_id);return move(i,status)
reset()
